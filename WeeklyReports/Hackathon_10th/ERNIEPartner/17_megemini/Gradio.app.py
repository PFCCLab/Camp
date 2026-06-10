import re
import os
import time
import socket
import signal
import random
import json
import subprocess
import threading
import openai
import gradio as gr

# ========== FastDeploy Server Config ==========

FD_MODEL = "baidu/ERNIE-4.5-0.3B-Paddle"
FD_HOST = "0.0.0.0"
FD_PORT = 8180
FD_METRICS_PORT = 8181
FD_WORKER_QUEUE_PORT = 8182
FD_MAX_MODEL_LEN = 32768
FD_MAX_NUM_SEQS = 32
FD_NUM_GPU_BLOCKS_OVERRIDE = 4896

fd_server_process = None
fd_server_log = []
client = None
active_backend = None  # None / "fastdeploy" / "openai"
model_name = "null"  # model string passed to the API

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0

def kill_process_on_port(port):
    try:
        result = subprocess.run(["lsof", "-t", "-i", f":{port}"], capture_output=True, text=True)
        pids = result.stdout.strip().split('\n')
        for pid_str in pids:
            pid_str = pid_str.strip()
            if pid_str:
                pid = int(pid_str)
                os.kill(pid, signal.SIGKILL)
                time.sleep(1)
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError, ProcessLookupError):
        try:
            subprocess.run(["fuser", "-k", f"{port}/tcp"], capture_output=True)
        except FileNotFoundError:
            pass

def read_server_log():
    global fd_server_process, fd_server_log
    if fd_server_process is None:
        return
    for line in iter(fd_server_process.stdout.readline, b""):
        decoded = line.decode("utf-8", errors="replace").rstrip()
        fd_server_log.append(decoded)
    for line in iter(fd_server_process.stderr.readline, b""):
        decoded = line.decode("utf-8", errors="replace").rstrip()
        fd_server_log.append(decoded)

def start_fd_server(model, host, port, metrics_port, worker_queue_port,
                    max_model_len, max_num_seqs, num_gpu_blocks_override):
    global fd_server_process, client, fd_server_log, active_backend, model_name
    if active_backend == "openai":
        disconnect_openai()
    if fd_server_process is not None and fd_server_process.poll() is None:
        return "Server is already running."

    if is_port_in_use(int(port)):
        kill_process_on_port(int(port))
        time.sleep(2)

    os.environ["ENABLE_V1_KVCACHE_SCHEDULER"] = "1"
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"

    cmd = [
        "python", "-m", "fastdeploy.entrypoints.openai.api_server",
        "--model", model,
        "--host", host,
        "--port", str(port),
        "--metrics-port", str(metrics_port),
        "--engine-worker-queue-port", str(worker_queue_port),
        "--max-model-len", str(max_model_len),
        "--max-num-seqs", str(max_num_seqs),
        "--num-gpu-blocks-override", str(num_gpu_blocks_override),
    ]
    fd_server_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    fd_server_log = []
    threading.Thread(target=read_server_log, daemon=True).start()
    client = openai.Client(base_url=f"http://{host}:{port}/v1", api_key="null")
    model_name = "null"
    active_backend = "fastdeploy"
    return f"Server started (PID: {fd_server_process.pid})"

def stop_fd_server():
    global fd_server_process, client, active_backend, model_name
    if fd_server_process is None or fd_server_process.poll() is not None:
        return "Server is not running."
    fd_server_process.terminate()
    try:
        fd_server_process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        fd_server_process.kill()
        fd_server_process.wait()
    fd_server_process = None
    client = None
    active_backend = None
    model_name = "null"
    return "Server stopped."

def get_fd_status():
    global fd_server_process
    if fd_server_process is None:
        return "stopped"
    rc = fd_server_process.poll()
    if rc is None:
        return "running"
    return f"exited (code: {rc})"

def check_fd_health():
    global client
    if client is None:
        return "Client not initialized."
    try:
        client.models.list()
        return "OK"
    except Exception as e:
        return f"Unreachable: {e}"

def get_fd_log():
    global fd_server_log
    return "\n".join(fd_server_log[-200:])

# ========== OpenAI API Backend ==========

OA_DEFAULT_BASE_URL = "https://api.openai.com/v1"
OA_DEFAULT_API_KEY = ""
OA_DEFAULT_MODEL = "gpt-4o-mini"

def connect_openai(base_url, api_key, oa_model):
    global client, active_backend, model_name
    if active_backend == "fastdeploy":
        stop_fd_server()
    if not base_url.strip():
        return "Base URL is required."
    if not api_key.strip():
        return "API key is required."
    try:
        client = openai.Client(base_url=base_url.rstrip("/"), api_key=api_key)
        client.models.list()
        model_name = oa_model.strip() or "gpt-4o-mini"
        active_backend = "openai"
        return f"Connected to {model_name} @ {base_url}"
    except Exception as e:
        client = None
        active_backend = None
        model_name = "null"
        return f"Connection failed: {e}"

def disconnect_openai():
    global client, active_backend, model_name
    client = None
    active_backend = None
    model_name = "null"
    return "Disconnected."

def get_oa_status():
    global active_backend
    if active_backend == "openai":
        return "connected"
    return "disconnected"

def check_oa_health():
    global client
    if client is None or active_backend != "openai":
        return "Not connected."
    try:
        client.models.list()
        return "OK"
    except Exception as e:
        return f"Unreachable: {e}"

def get_active_backend_label():
    global active_backend
    if active_backend == "fastdeploy":
        return "FastDeploy (local)"
    if active_backend == "openai":
        return "OpenAI API (remote)"
    return "None"

# ========== Game Config ==========

DIFFICULTY_MULTIPLIERS = {1: 1.0, 2: 1.2, 3: 1.5, 4: 2.0, 5: 2.5}
DIFFICULTY_TIME_LIMITS = {1: 30, 2: 25, 3: 20, 4: 18, 5: 15}
DIFFICULTY_SENTENCE_LENGTH = {1: 10, 2: 20, 3: 30, 4: 40, 5: 50}
BASE_SCORE = 10
TIME_BONUS_FACTOR = 0.5
STREAK_BONUS = 2
TIMED_MODE_QUESTIONS = 10
MAX_RETRIES = 2

# ========== Question Generation ==========

def build_sentence_prompt(difficulty):
    target_len = DIFFICULTY_SENTENCE_LENGTH.get(difficulty, 12)
    return f"请生成一句约 {target_len} 个词的英文句子。"

def generate_sentence(difficulty):
    prompt = build_sentence_prompt(difficulty)
    for attempt in range(MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8, top_p=0.95, max_tokens=128, stream=False,
            )
            text = response.choices[0].message.content.strip()
            if text and len(text.split()) >= 4:
                return text
        except Exception as e:
            print(f"generate_sentence: error (attempt {attempt + 1}): {e}")
    return ""

def _is_valid_english_word(w):
    if not isinstance(w, str) or not w.strip():
        return False
    if re.search(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]', w):
        return False
    if re.match(r'option\d+$', w, re.IGNORECASE):
        return False
    if re.match(r'^[a-zA-Z\'-]+$', w) is None:
        return False
    return True

def get_synonyms(word):
    prompt = f"""请为英文单词 "{word}" 提供 5 个同义词或近义词。以 json 格式返回
{{
    "synonyms": [
    ]
}}"""
    for attempt in range(MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6, top_p=0.9, max_tokens=128, stream=False,
            )
            text = response.choices[0].message.content.strip()
            try:
                data = json.loads(text)
                syns = data.get("synonyms", [])
            except json.JSONDecodeError:
                match = re.search(r'\{[\s\S]*?\}', text)
                if match:
                    try:
                        data = json.loads(match.group())
                        syns = data.get("synonyms", [])
                    except json.JSONDecodeError:
                        syns = []
                else:
                    syns = []
            syns = [w for w in syns if isinstance(w, str) and w.lower() != word.lower()]
            syns = [w for w in syns if _is_valid_english_word(w)]
            if len(syns) < 2:
                raise ValueError("not enough valid English synonyms")
            return random.sample(syns, 2)
        except Exception as e:
            print(f"get_synonyms('{word}'): error (attempt {attempt + 1}): {e}")
    return []

def pick_cloze_word(sentence):
    skip_words = {
        'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'am', 'do', 'does', 'did', 'have', 'has', 'had', 'having',
        'will', 'would', 'shall', 'should', 'can', 'could', 'may', 'might', 'must',
        'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
        'my', 'your', 'his', 'its', 'our', 'their', 'mine', 'yours', 'hers', 'ours',
        'this', 'that', 'these', 'those',
        'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'up', 'down',
        'out', 'off', 'over', 'under', 'about', 'into', 'through', 'after', 'before',
        'between', 'among', 'during', 'until', 'since',
        'and', 'or', 'but', 'not', 'nor', 'so', 'yet', 'if', 'then',
        'as', 'than', 'when', 'while', 'where', 'how', 'what', 'which', 'who',
        'very', 'too', 'also', 'just', 'only', 'even', 'still', 'already',
        'no', 'yes', 'all', 'each', 'every', 'both', 'any', 'some',
        'here', 'there', 'now', 'never', 'always', 'often',
    }
    words = []
    for match in re.finditer(r"[a-zA-Z']+", sentence):
        words.append((match.group(), match.start(), match.end()))
    candidates = [(w, s, e) for w, s, e in words if w.lower() not in skip_words and len(w) >= 3]
    if not candidates:
        candidates = [(w, s, e) for w, s, e in words if w.lower() not in skip_words and len(w) >= 2]
    if not candidates:
        return None
    chosen = random.choice(candidates)
    return chosen[0], chosen[1], chosen[2]

def build_cloze_question(sentence, word, start, end, synonyms):
    answer = word
    options = [answer]
    for syn in synonyms:
        if syn.lower() != answer.lower() and syn not in options:
            options.append(syn)
    while len(options) < 3:
        options.append(f"option{len(options)}")
    options = options[:3]
    random.shuffle(options)
    options_str = ', '.join(options)
    question_text = sentence[:start] + f'[{options_str}]' + sentence[end:]
    return question_text, options, answer

def get_question(difficulty):
    for attempt in range(MAX_RETRIES + 1):
        try:
            sentence = generate_sentence(difficulty)
            sentence = sentence.strip('"\'')
            if not sentence or len(sentence.split()) < 4:
                continue
            pick_result = pick_cloze_word(sentence)
            if pick_result is None:
                continue
            word, start, end = pick_result
            synonyms = get_synonyms(word)
            if len(synonyms) < 2:
                continue
            question_text, options, answer = build_cloze_question(sentence, word, start, end, synonyms)
            return question_text, options, answer
        except Exception as e:
            print(f"Error generating question (attempt {attempt + 1}): {e}")
    return None

# ========== Game State ==========

class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.score = 0
        self.difficulty = 1
        self.streak = 0
        self.mode = "arcade"
        self.remaining_questions = TIMED_MODE_QUESTIONS
        self.total_correct = 0
        self.current_question = None
        self.game_active = False
        self.start_time = 0

    def get_time_limit(self):
        return DIFFICULTY_TIME_LIMITS.get(min(self.difficulty, 5), 15)

    def calculate_score(self, time_remaining):
        diff_key = min(self.difficulty, 5)
        multiplier = DIFFICULTY_MULTIPLIERS[diff_key]
        time_bonus = time_remaining * TIME_BONUS_FACTOR
        streak_bonus = self.streak * STREAK_BONUS
        total = int(BASE_SCORE * multiplier + time_bonus + streak_bonus)
        return max(total, 1)

game = GameState()

# ========== Countdown Timer HTML ==========

TIMEOUT_SENTINEL = "__TIMEOUT__"

_timer_counter = 0

def build_timer_html(time_limit, mode="arcade"):
    global _timer_counter
    if mode != "timed":
        return "<div></div>"
    # CSS-only countdown: no <script> tags (Gradio strips them).
    # Uses @keyframes animation + CSS counter to visually decrement.
    # The actual timeout is handled server-side via gr.Timer.
    # A unique suffix per call forces the browser to treat each update as a
    # fresh animation (same id/name would cause the browser to skip restart).
    _timer_counter += 1
    uid = _timer_counter
    steps_css = ""
    for i in range(time_limit, -1, -1):
        pct = (time_limit - i) / time_limit * 100
        steps_css += f"  {pct:.4f}% {{ counter-set: tick{uid} {i}; }}\n"
    return f"""<style>
@keyframes countdown{uid} {{
{steps_css}}}
#cd-wrap{uid} {{
  text-align: center; padding: 8px;
  font-size: 28px; font-weight: bold; font-family: monospace;
  counter-reset: tick{uid} {time_limit};
  animation: countdown{uid} {time_limit}s linear forwards;
}}
#cd-wrap{uid}::after {{ content: counter(tick{uid}) "s"; }}
</style>
<div id="cd-wrap{uid}"></div>"""

# ========== Gradio Callbacks ==========

def start_game(mode_choice):
    game.reset()
    game.mode = mode_choice
    game.game_active = True

    question_data = get_question(game.difficulty)
    if question_data is None:
        return (
            "Failed to generate question. Please try again.",
            gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),
            "", "", "", "", "",
            build_timer_html(0),
        )

    game.current_question = question_data
    game.start_time = time.time()

    q_text, options, answer = question_data
    display_text = re.sub(r'\[[^\]]+\]', '___', q_text)

    time_limit = game.get_time_limit()
    if game.mode == "arcade":
        info = f"Arcade | Diff: {game.difficulty} | Time: {time_limit}s"
    else:
        info = f"Timed | Q: 0/{TIMED_MODE_QUESTIONS} | Time: {time_limit}s"

    return (
        display_text,
        gr.update(value=options[0], visible=True),
        gr.update(value=options[1], visible=True),
        gr.update(value=options[2], visible=True),
        str(game.score), str(game.streak), str(game.difficulty),
        info, "",
        build_timer_html(time_limit, game.mode),
    )

def handle_answer(selected_option):
    if not game.game_active or game.current_question is None:
        return (
            "Game is not active. Please start a new game.",
            gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),
            "", "", "", "", "",
            build_timer_html(0),
        )

    q_text, options, correct_answer = game.current_question
    elapsed = time.time() - game.start_time
    time_remaining = max(game.get_time_limit() - elapsed, 0)
    is_timeout = (selected_option == TIMEOUT_SENTINEL)
    is_correct = False if is_timeout else (selected_option == correct_answer)

    def fail(msg):
        feedback = msg
        if game.mode == "arcade":
            game.game_active = False
            summary = (
                f"\n--- GAME OVER ---\n"
                f"Final Score: {game.score} | Max Streak: {game.streak} | "
                f"Difficulty Reached: {game.difficulty}"
            )
            return (
                feedback + summary,
                gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),
                str(game.score), str(game.streak), str(game.difficulty),
                "Game Over", "",
                build_timer_html(0),
            )
        else:
            game.remaining_questions -= 1
            if game.remaining_questions <= 0:
                game.game_active = False
                summary = (
                    f"\n--- ALL QUESTIONS DONE ---\n"
                    f"Final Score: {game.score} | Correct: {game.total_correct}/{TIMED_MODE_QUESTIONS}"
                )
                return (
                    feedback + summary,
                    gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),
                    str(game.score), str(game.streak), str(game.difficulty),
                    "Game Over", "",
                    build_timer_html(0),
                )
            return _next_question(feedback)

    def _next_question(feedback):
        question_data = get_question(game.difficulty)
        if question_data is None:
            game.game_active = False
            return (
                feedback + "\nFailed to generate next question. Game ended.",
                gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),
                str(game.score), str(game.streak), str(game.difficulty),
                "Error", "",
                build_timer_html(0),
            )

        game.current_question = question_data
        game.start_time = time.time()

        new_q_text, new_options, _ = question_data
        display_text = re.sub(r'\[[^\]]+\]', '___', new_q_text)
        time_limit = game.get_time_limit()

        if game.mode == "arcade":
            info = f"Arcade | Diff: {game.difficulty} | Time: {time_limit}s | Streak: {game.streak}"
        else:
            info = f"Timed | Q: {game.total_correct}/{TIMED_MODE_QUESTIONS - game.remaining_questions} | Time: {time_limit}s"

        return (
            display_text,
            gr.update(value=new_options[0], visible=True),
            gr.update(value=new_options[1], visible=True),
            gr.update(value=new_options[2], visible=True),
            str(game.score), str(game.streak), str(game.difficulty),
            info, feedback,
            build_timer_html(time_limit, game.mode),
        )

    if not is_correct:
        msg = "Time's up! " if is_timeout else ""
        msg += f"The correct answer is: {correct_answer}"
        return fail(msg)

    if game.mode == "arcade":
        game.streak += 1
        earned = game.calculate_score(time_remaining)
        game.score += earned
        feedback = f"Correct! +{earned} points (Time bonus: {time_remaining:.1f}s)"
        if game.difficulty < 5:
            game.difficulty += 1
    else:
        game.remaining_questions -= 1
        game.total_correct += 1
        game.streak += 1
        earned = game.calculate_score(time_remaining)
        game.score += earned
        feedback = f"Correct! +{earned} points (Time bonus: {time_remaining:.1f}s)"
        if game.difficulty < 5:
            game.difficulty += 1

        if game.remaining_questions <= 0:
            game.game_active = False
            summary = (
                f"\n--- ALL QUESTIONS DONE ---\n"
                f"Final Score: {game.score} | Correct: {game.total_correct}/{TIMED_MODE_QUESTIONS}"
            )
            return (
                feedback + summary,
                gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),
                str(game.score), str(game.streak), str(game.difficulty),
                "Game Over", "",
                build_timer_html(0),
            )

    return _next_question(feedback)

# ========== Gradio UI ==========

with gr.Blocks(title="English Cloze Challenge", theme=gr.themes.Soft()) as demo:
    with gr.Tabs():
        # ==================== Game Tab ====================
        with gr.Tab("Game"):
            gr.Markdown("# English Cloze Challenge")
            backend_label = gr.Textbox(label="Active Backend", value=get_active_backend_label(), interactive=False)
            gr.Markdown("Select a game mode and answer cloze questions to earn points!")

            with gr.Row():
                with gr.Column(scale=1):
                    mode_radio = gr.Radio(
                        choices=["arcade", "timed"],
                        value="timed",
                        label="Game Mode",
                        info="Arcade: game over on wrong answer | Timed: answer 10 questions",
                    )
                    start_btn = gr.Button("Start Game", variant="primary")

                with gr.Column(scale=2):
                    info_text = gr.Textbox(label="Game Info", interactive=False)
                    feedback_text = gr.Textbox(label="Feedback", interactive=False)

            time_display = gr.HTML(build_timer_html(0))

            question_display = gr.Textbox(label="Question", lines=3, interactive=False)
            timeout_btn = gr.Button("Timeout", elem_id="timeout_btn", visible=False)

            with gr.Row():
                opt1_btn = gr.Button("Option 1", visible=False)
                opt2_btn = gr.Button("Option 2", visible=False)
                opt3_btn = gr.Button("Option 3", visible=False)

            gr.Markdown("---")

            with gr.Row():
                score_display = gr.Textbox(label="Score", value="0", interactive=False)
                streak_display = gr.Textbox(label="Streak", value="0", interactive=False)
                diff_display = gr.Textbox(label="Difficulty", value="1", interactive=False)

            gr.Markdown("---")

            gr.Markdown("""> 此 Gradio app 基于 RFC: https://aistudio.baidu.com/projectdetail/10237267
                        
## 如何游玩

**1. 先设置后端** — 前往 **设置** 选项卡，选择一个后端并确保连接成功后再开始游戏。

| 后端 | 使用方法 |
|---------|-----------|
| FastDeploy（本地） | 点击 **启动服务器**，等待状态显示为 `running`，然后点击 **健康检查** 确认 `OK` |
| OpenAI API（远程） | 填写 Base URL、API Key 和模型名称，然后点击 **连接** |

**2. 游戏规则**

| | 限时模式 | 街机模式 |
|---|---|---|
| 目标 | 回答 10 道题 | 尽可能长时间存活 |
| 答错/超时 | 标记为错误，进入下一题 | 立即结束游戏 |
| 难度 | 答对后提升（1→5） | 答对后提升（1→5） |

**3. 计分规则**

- `得分 = 10 × 难度倍率 + 剩余时间 × 0.5 + 连击数 × 2`
- 难度倍率：1.0× / 1.2× / 1.5× / 2.0× / 2.5×（对应难度 1–5）
- 回答越快，时间奖励越高；连续答对可获得连击加分

**4. 难度等级**

| 等级 | 句子长度 | 时间限制 | 倍率 |
|-------|----------------|------------|------------|
| 1 | 约 10 词 | 30 秒 | 1.0× |
| 2 | 约 20 词 | 25 秒 | 1.2× |
| 3 | 约 30 词 | 20 秒 | 1.5× |
| 4 | 约 40 词 | 18 秒 | 2.0× |
| 5 | 约 50 词 | 15 秒 | 2.5× |
""")

            all_outputs = [
                question_display,
                opt1_btn, opt2_btn, opt3_btn,
                score_display, streak_display, diff_display,
                info_text, feedback_text,
                time_display,
            ]

            # --- Server-side timeout via gr.Timer ---
            # A 1-second timer checks if the timed-mode question has expired.
            timeout_timer = gr.Timer(value=1, active=False)

            def check_timeout():
                """Called every 1s by timeout_timer. If time is up in timed mode,
                trigger the timeout handler; otherwise return no-op updates."""
                if not game.game_active or game.mode != "timed":
                    return tuple(gr.update() for _ in all_outputs) + (gr.Timer(active=False),)
                if game.current_question is None:
                    return tuple(gr.update() for _ in all_outputs) + (gr.Timer(active=False),)
                elapsed = time.time() - game.start_time
                if elapsed >= game.get_time_limit():
                    result = handle_answer(TIMEOUT_SENTINEL)
                    # Stop timer if game ended after timeout
                    still_active = game.game_active and game.mode == "timed"
                    return result + (gr.Timer(active=still_active),)
                return tuple(gr.update() for _ in all_outputs) + (gr.update(),)

            timeout_timer.tick(
                fn=check_timeout,
                outputs=all_outputs + [timeout_timer],
            )

            def start_game_and_activate_timer(mode_choice):
                result = start_game(mode_choice)
                # Only activate the server-side timer in timed mode
                timer_active = game.game_active and game.mode == "timed"
                return result + (gr.Timer(active=timer_active),)

            start_btn.click(
                fn=start_game_and_activate_timer,
                inputs=[mode_radio],
                outputs=all_outputs + [timeout_timer],
            )

            def handle_answer_and_maybe_stop_timer(selected_option):
                result = handle_answer(selected_option)
                # Stop the timer if game is no longer active or not in timed mode
                should_stop = not (game.game_active and game.mode == "timed")
                return result + (gr.Timer(active=not should_stop),)

            for btn in [opt1_btn, opt2_btn, opt3_btn]:
                btn.click(
                    fn=handle_answer_and_maybe_stop_timer,
                    inputs=[btn],
                    outputs=all_outputs + [timeout_timer],
                )

            timeout_btn.click(
                fn=handle_answer,
                inputs=[gr.State(TIMEOUT_SENTINEL)],
                outputs=all_outputs,
            )

        # ==================== Settings Tab ====================
        with gr.Tab("Settings"):
            gr.Markdown("## Backend Settings")
            gr.Markdown("Choose one backend. Activating one will automatically deactivate the other.")

            backend_radio = gr.Radio(
                choices=["FastDeploy (local)", "OpenAI API (remote)"],
                value="FastDeploy (local)",
                label="Backend Type",
            )

            # --- FastDeploy section ---
            with gr.Column(visible=True) as fd_panel:
                gr.Markdown("### FastDeploy Server")
                fd_status = gr.Textbox(label="Server Status", value=get_fd_status(), interactive=False)
                refresh_fd_btn = gr.Button("Refresh Status")

                with gr.Accordion("Server Configuration", open=False):
                    fd_model_box = gr.Textbox(label="Model Path", value=FD_MODEL)
                    with gr.Row():
                        fd_host_box = gr.Textbox(label="Host", value=FD_HOST)
                        fd_port_box = gr.Number(label="Port", value=FD_PORT, precision=0)
                    with gr.Row():
                        fd_metrics_port_box = gr.Number(label="Metrics Port", value=FD_METRICS_PORT, precision=0)
                        fd_wq_port_box = gr.Number(label="Worker Queue Port", value=FD_WORKER_QUEUE_PORT, precision=0)
                    with gr.Row():
                        fd_max_len_box = gr.Number(label="Max Model Len", value=FD_MAX_MODEL_LEN, precision=0)
                        fd_max_seqs_box = gr.Number(label="Max Num Seqs", value=FD_MAX_NUM_SEQS, precision=0)
                        fd_gpu_blocks_box = gr.Number(label="Num GPU Blocks Override", value=FD_NUM_GPU_BLOCKS_OVERRIDE, precision=0)

                with gr.Row():
                    start_fd_btn = gr.Button("Start Server", variant="primary")
                    stop_fd_btn = gr.Button("Stop Server", variant="stop")
                    health_fd_btn = gr.Button("Health Check")

                fd_msg = gr.Textbox(label="Server Message", interactive=False)
                gr.Markdown("**Server Log**")
                fd_log = gr.Textbox(label="Log Output", lines=10, max_lines=25, interactive=False)
                log_refresh_btn = gr.Button("Refresh Log")

            # --- OpenAI API section ---
            with gr.Column(visible=False) as oa_panel:
                gr.Markdown("### OpenAI-Compatible API")
                oa_status = gr.Textbox(label="Connection Status", value=get_oa_status(), interactive=False)
                refresh_oa_btn = gr.Button("Refresh Status")

                with gr.Row():
                    oa_base_url = gr.Textbox(label="Base URL", value=OA_DEFAULT_BASE_URL)
                    oa_api_key = gr.Textbox(label="API Key", type="password", value=OA_DEFAULT_API_KEY)
                oa_model = gr.Textbox(label="Model Name", value=OA_DEFAULT_MODEL)

                with gr.Row():
                    connect_oa_btn = gr.Button("Connect", variant="primary")
                    disconnect_oa_btn = gr.Button("Disconnect", variant="stop")
                    health_oa_btn = gr.Button("Health Check")

                oa_msg = gr.Textbox(label="Connection Message", interactive=False)

            # --- Radio toggles panel visibility ---
            backend_radio.change(
                fn=lambda choice: (gr.update(visible=(choice == "FastDeploy (local)")),
                                   gr.update(visible=(choice == "OpenAI API (remote)"))),
                inputs=[backend_radio],
                outputs=[fd_panel, oa_panel],
            )

            # --- FastDeploy event bindings ---
            refresh_fd_btn.click(fn=lambda: get_fd_status(), outputs=[fd_status])

            start_fd_btn.click(
                fn=start_fd_server,
                inputs=[fd_model_box, fd_host_box, fd_port_box,
                        fd_metrics_port_box, fd_wq_port_box,
                        fd_max_len_box, fd_max_seqs_box, fd_gpu_blocks_box],
                outputs=[fd_msg],
            ).then(fn=lambda: get_fd_status(), outputs=[fd_status]
            ).then(fn=get_active_backend_label, outputs=[backend_label])

            stop_fd_btn.click(
                fn=stop_fd_server,
                outputs=[fd_msg],
            ).then(fn=lambda: get_fd_status(), outputs=[fd_status]
            ).then(fn=get_active_backend_label, outputs=[backend_label])

            health_fd_btn.click(fn=check_fd_health, outputs=[fd_msg])

            log_refresh_btn.click(fn=get_fd_log, outputs=[fd_log])

            # --- OpenAI event bindings ---
            refresh_oa_btn.click(fn=lambda: get_oa_status(), outputs=[oa_status])

            connect_oa_btn.click(
                fn=connect_openai,
                inputs=[oa_base_url, oa_api_key, oa_model],
                outputs=[oa_msg],
            ).then(fn=lambda: get_oa_status(), outputs=[oa_status]
            ).then(fn=get_active_backend_label, outputs=[backend_label])

            disconnect_oa_btn.click(
                fn=disconnect_openai,
                outputs=[oa_msg],
            ).then(fn=lambda: get_oa_status(), outputs=[oa_status]
            ).then(fn=get_active_backend_label, outputs=[backend_label])

            health_oa_btn.click(fn=check_oa_health, outputs=[oa_msg])

demo.launch()

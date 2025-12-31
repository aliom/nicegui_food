import uuid
import random
import math
import colorsys
import asyncio
from datetime import datetime
from typing import Dict, List, Optional
from nicegui import ui, app

# ==============================================================================
# 1. VISUAL STYLE: BRIGHT PIXEL PICNIC
# ==============================================================================

FONT_URL = "https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap"

CSS_STYLES = f"""
    @import url('{FONT_URL}');

    :root {{
        /* Bright Palette */
        --bg-color: #55efc4; /* Mint Green */
        --bg-pattern: #00b894; /* Darker Mint */
        --card-white: #ffffff;
        --accent-yellow: #ffeaa7;
        --accent-pink: #fd79a8;
        --accent-blue: #74b9ff;
        --text-dark: #2d3436;
        --border-color: #2d3436;
        --shadow-hard: 4px 4px 0px #000;
    }}

    body {{
        font-family: 'Press Start 2P', cursive;
        background-color: var(--bg-color);
        /* Polka Dot Pattern */
        background-image: radial-gradient(var(--bg-pattern) 15%, transparent 16%),
                          radial-gradient(var(--bg-pattern) 15%, transparent 16%);
        background-size: 20px 20px;
        background-position: 0 0, 10px 10px;
        color: var(--text-dark);
        margin: 0;
        overflow-x: hidden;
        /* 45度角无限移动动画 */
        animation: polka-dot-move 3s linear infinite;
    }}
    
    @keyframes polka-dot-move {{
        0% {{
            background-position: 0 0, 10px 10px;
        }}
        100% {{
            /* 45度角移动：x和y方向都移动20px（一个完整的周期）实现无缝循环 */
            background-position: 20px 20px, 30px 30px;
        }}
    }}

    /* Funky Button */
    .funky-btn {{
        font-family: 'Press Start 2P';
        border: 3px solid #000;
        box-shadow: var(--shadow-hard);
        text-transform: uppercase;
        padding: 12px 20px;
        cursor: pointer;
        transition: transform 0.1s;
        text-align: center;
    }}
    .funky-btn:active {{ transform: translate(2px, 2px); box-shadow: 2px 2px 0 #000; }}
    
    .btn-pink {{ background-color: var(--accent-pink); color: white; }}
    .btn-yellow {{ background-color: var(--accent-yellow); color: black; }}
    .btn-blue {{ background-color: var(--accent-blue); color: white; }}

    /* Input Field */
    .comic-input {{
        border: 3px solid #000;
        box-shadow: 4px 4px 0 rgba(0,0,0,0.2);
        font-family: 'VT323';
        font-size: 1.8rem;
        text-align: center;
        padding: 5px;
        background: white;
        color: black;
        outline: none;
    }}

    /* ================= CARD ANIMATIONS & LAYOUT ================= */
    
    /* 1. Entrance Animation (Slide up from bottom) */
    @keyframes slide-in-elastic {{
        0% {{ transform: translateY(100vh) scale(0.5) rotate(0deg); opacity: 0; }}
        60% {{ transform: translateY(-20px) scale(1.1) rotate(5deg); opacity: 1; }}
        100% {{ transform: translateY(0) scale(1) rotate(var(--target-rotation)); }}
    }}

    .card-entry {{
        animation: slide-in-elastic 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
        will-change: transform, opacity;
    }}
    
    .card-entry-done {{
        /* No animation, just final state with rotation */
        transform: rotate(var(--target-rotation));
    }}
    
    /* Card flip animation */
    @keyframes card-flip {{
        0% {{ transform: rotateY(0deg); }}
        50% {{ transform: rotateY(90deg); }}
        100% {{ transform: rotateY(0deg); }}
    }}
    
    .card-flipping {{
        animation: card-flip 0.5s ease-in-out;
    }}

    /* 2. Card Visuals */
    .messy-card {{
        width: 140px;
        height: 190px;
        background-color: white;
        border: 3px solid black;
        border-radius: 12px;
        /* Variable rotation is set via inline style in Python */
        position: relative;
        cursor: pointer;
        transition: transform 0.2s;
        box-shadow: 3px 3px 0 rgba(0,0,0,0.2);
    }}
    
    .messy-card:hover {{
        z-index: 50;
        transform: scale(1.1) rotate(0deg) !important; /* Straighten on hover */
        box-shadow: 10px 10px 0 rgba(0,0,0,0.3);
    }}

    .card-content {{
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 8px;
        word-break: break-word;
    }}

    /* Card Back (Hidden State) - color will be set dynamically */
    .card-back-pattern {{
        background-image: linear-gradient(45deg, rgba(255,255,255,0.3) 25%, transparent 25%, transparent 75%, rgba(255,255,255,0.3) 75%, rgba(255,255,255,0.3)), 
                          linear-gradient(45deg, rgba(255,255,255,0.3) 25%, transparent 25%, transparent 75%, rgba(255,255,255,0.3) 75%, rgba(255,255,255,0.3));
        background-size: 20px 20px;
        background-position: 0 0, 10px 10px;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        text-shadow: 2px 2px 0 #000;
    }}

    /* ================= LOTTERY EFFECT ================= */
    .slot-machine-overlay {{
        background: rgba(0,0,0,0.85);
        backdrop-filter: blur(5px);
    }}
    
    .slot-text {{
        font-size: 3rem;
        font-weight: bold;
        text-shadow: 4px 4px 0 #000;
    }}
    
    .winner-bounce {{
        animation: bounce-in 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}
    
    @keyframes bounce-in {{
        0% {{ transform: scale(0); }}
        50% {{ transform: scale(1.5); }}
        100% {{ transform: scale(1); }}
    }}
    
    /* Instruction Box */
    .instruction-box {{
        background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
        border: 3px solid #000;
        box-shadow: 4px 4px 0 rgba(0,0,0,0.2);
        padding: 16px;
        border-radius: 8px;
        font-family: 'VT323', monospace;
        font-size: 1.2rem;
        line-height: 1.6;
    }}
    
    /* Arrow Tooltip */
    .arrow-tooltip-container {{
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 8px;
    }}
    
    .tooltip-text {{
        background: var(--accent-pink);
        color: white;
        padding: 8px 16px;
        border: 2px solid #000;
        border-radius: 6px;
        font-family: 'VT323', monospace;
        font-size: 1.4rem;
        white-space: nowrap;
        box-shadow: 3px 3px 0 rgba(0,0,0,0.3);
        margin-bottom: 4px;
    }}
    
    .arrow-down {{
        font-size: 2.5rem;
        color: var(--accent-pink);
        text-shadow: 2px 2px 0 #000;
        line-height: 1;
        animation: bounce-arrow 1.5s ease-in-out infinite;
    }}
    
    @keyframes bounce-arrow {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-8px); }}
    }}
"""

# ==============================================================================
# 2. LOGIC & DATA MODELS
# ==============================================================================

FUNNY_PHRASES = ["Don't Peek!", "Secret Sauce", "Diet Starts Tmrw", "Yummy?", "No Pineapple", "Spicy!", "Mom's Pick"]

class Card:
    def __init__(self, content: str, owner_id: str, owner_color: str):
        self.id = str(uuid.uuid4())
        self.content = content
        self.owner_id = owner_id
        self.color = owner_color
        # Each card gets a permanent random rotation for the "Messy Table" look
        self.rotation = random.randint(-6, 6) 
        self.back_text = random.choice(FUNNY_PHRASES)
        # Track if card has been flipped by clicking
        self.is_flipped = False
        # Track if card has already played entrance animation
        self.has_animated = False

class User:
    def __init__(self, uid: str, nickname: str, color: str):
        self.uid = uid
        self.nickname = nickname
        self.color = color
        self.cards: List[Card] = []

class Room:
    def __init__(self, room_id: str, host_id: str):
        self.room_id = room_id
        self.host_id = host_id
        self.users: Dict[str, User] = {}
        self.all_cards: List[Card] = []
        self.last_update = datetime.now()
        # State for the lottery animation
        self.is_rolling = False 
        self.current_roll_text = "..." 
        self.winner_card: Optional[Card] = None
        # Track which users have closed the overlay
        self.overlay_closed_by: set = set()
        # Track which card each user has flipped (one card per user at a time)
        self.user_flipped_card: Dict[str, Optional[str]] = {}  # user_id -> card_id
        # Lottery animation state
        self.lottery_phase_index = 0
        self.lottery_phases = []
        self.lottery_options = []
        self.lottery_tick_count = 0

    def touch(self):
        self.last_update = datetime.now()

rooms: Dict[str, Room] = {}

def get_bright_color() -> str:
    """Generate bright, cartoonish colors"""
    colors = [
        '#ff7675', '#74b9ff', '#55efc4', '#a29bfe', '#ffeaa7', 
        '#fab1a0', '#fd79a8', '#00b894', '#0984e3', '#e84393'
    ]
    return random.choice(colors)

# ==============================================================================
# 3. UI PAGES
# ==============================================================================

@ui.page('/')
def login_page():
    ui.add_head_html(f'<style>{CSS_STYLES}</style>')

    with ui.column().classes('w-full h-screen items-center justify-center'):
        # Fun Title
        with ui.column().classes('items-center mb-8 gap-0'):
            ui.label('WHAT TO').classes('text-3xl font-black text-white stroke-black').style('-webkit-text-stroke: 2px black; text-shadow: 4px 4px 0 #000;')
            ui.label('EAT?!').classes('text-6xl font-black text-[#ffeaa7]').style('-webkit-text-stroke: 3px black; text-shadow: 6px 6px 0 #000;')
            ui.label('The indecision killer').classes('text-sm mt-2 font-bold bg-black text-white px-2 py-1 rotate-[-2deg]')

        # Card Container
        with ui.card().classes('w-80 bg-white border-[3px] border-black shadow-[8px_8px_0_rgba(0,0,0,0.2)] p-6 items-center gap-4'):
            
            room_in = ui.input(placeholder='Room Code #').props('input-class="comic-input"').classes('w-full')
            name_in = ui.input(placeholder='Nick Name').props('input-class="comic-input"').classes('w-full')
            
            def go():
                rid = room_in.value.strip().upper()
                name = name_in.value.strip()
                if not rid or not name: 
                    ui.notify('Hey! Fill in the blanks! 😡', color='red')
                    return
                
                uid = str(uuid.uuid4())
                app.storage.user['uid'] = uid
                
                if rid not in rooms: rooms[rid] = Room(rid, uid)
                room = rooms[rid]
                
                if uid not in room.users:
                    # Assign random bright color
                    room.users[uid] = User(uid, name, get_bright_color())
                    room.touch()
                
                ui.navigate.to(f'/room/{rid}')

            ui.button('LET\'S GO!', on_click=go).classes('funky-btn btn-pink w-full text-xl font-bold')
        
        # 使用说明
        with ui.card().classes('w-80 mt-4 instruction-box'):
            with ui.column().classes('gap-3'):
                ui.label('📖 使用说明').classes('text-xl font-bold mb-1').style('font-family: "Press Start 2P", cursive; font-size: 0.9rem; line-height: 1.5;')
                with ui.column().classes('gap-1.5'):
                    ui.label('1. 输入您的昵称，输入与朋友相同的房间号并进入').classes('text-base').style('font-family: "VT323", monospace;')
                    ui.label('2. 添加 3 项你想吃的餐厅').classes('text-base').style('font-family: "VT323", monospace;')
                    ui.label('3. 开启抽签！或等待房主开始抽签').classes('text-base').style('font-family: "VT323", monospace;')

@ui.page('/room/{room_id}')
def room_page(room_id: str):
    ui.add_head_html(f'<style>{CSS_STYLES}</style>')
    
    if room_id not in rooms: ui.navigate.to('/'); return
    uid = app.storage.user.get('uid')
    if not uid or uid not in rooms[room_id].users: ui.navigate.to('/'); return

    room = rooms[room_id]
    user = room.users[uid]
    
    input_state = {'text': ''}

    # --- ACTIONS ---
    
    def add_card():
        val = input_state['text'].strip()
        if not val: return
        # Limit to 3 cards
        if len(user.cards) >= 3: 
            ui.notify('Woah there! 3 ideas max! 🐷', color='orange')
            return
            
        new_c = Card(val, user.uid, user.color)
        user.cards.append(new_c)
        room.all_cards.append(new_c)
        input_state['text'] = ''
        room.touch()
    
    def delete_card(card_obj):
        if card_obj in room.all_cards:
            room.all_cards.remove(card_obj)
            user.cards = [c for c in user.cards if c.id != card_obj.id]
            room.touch()
    
    def flip_card(card_obj):
        """Flip a card when clicked - only one card can be flipped at a time per user"""
        # Get the currently flipped card for this user
        current_flipped_card_id = room.user_flipped_card.get(user.uid)
        
        # If there's a currently flipped card and it's different from the one being clicked
        if current_flipped_card_id and current_flipped_card_id != card_obj.id:
            # Find and close the previously flipped card
            for card in room.all_cards:
                if card.id == current_flipped_card_id:
                    card.is_flipped = False
                    break
        
        # Toggle the clicked card
        card_obj.is_flipped = not card_obj.is_flipped
        
        # Update the tracking dictionary
        if card_obj.is_flipped:
            room.user_flipped_card[user.uid] = card_obj.id
        else:
            room.user_flipped_card[user.uid] = None
        
        room.touch()

    # --- LOTTERY LOGIC (SLOT MACHINE STYLE) ---
    def start_lottery():
        if not room.all_cards: return
        if room.is_rolling: return  # Prevent multiple simultaneous lotteries
        
        # 1. Initialize lottery state
        room.is_rolling = True
        room.winner_card = None
        room.current_roll_text = "..."
        room.lottery_options = [c.content for c in room.all_cards]
        
        # 2. Prepare phases for animation
        # Each number represents how many timer ticks (0.05s each) to wait before next update
        phase_delays = [1] * 20 + [2] * 10 + [4] * 5 + [8] * 3  # Convert seconds to timer ticks
        room.lottery_phases = phase_delays
        room.lottery_phase_index = 0
        room.lottery_tick_count = 0
        room.touch() # Trigger UI update for everyone
    
    def update_lottery():
        """Update lottery animation - called by timer"""
        if not room.is_rolling:
            return
        
        if room.lottery_phase_index < len(room.lottery_phases):
            # Check if we should update this tick
            current_phase_delay = room.lottery_phases[room.lottery_phase_index]
            room.lottery_tick_count += 1
            
            if room.lottery_tick_count >= current_phase_delay:
                # Time to update - show random option
                room.current_roll_text = random.choice(room.lottery_options)
                room.lottery_phase_index += 1
                room.lottery_tick_count = 0
                room.touch()
        else:
            # Animation complete - select winner
            room.winner_card = random.choice(room.all_cards)
            room.current_roll_text = room.winner_card.content
            room.is_rolling = False
            room.lottery_phase_index = 0
            room.lottery_tick_count = 0
            room.touch()

    def reset_game():
        room.winner_card = None
        room.is_rolling = False
        room.overlay_closed_by.clear()
        room.user_flipped_card.clear()  # Clear all flipped card states
        # Reset all cards' flipped state before clearing
        for card in room.all_cards:
            card.is_flipped = False
        room.all_cards = []
        for u in room.users.values(): u.cards = []
        room.touch()
    
    def restart_lottery():
        """Restart lottery without clearing cards"""
        room.winner_card = None
        room.is_rolling = False
        room.overlay_closed_by.clear()
        room.touch()

    # --- MAIN UI RENDERER ---
    
    @ui.refreshable
    def render_table():
        # Full screen layout
        with ui.column().classes('w-full min-h-screen items-center p-4 pb-32 relative'):
            
            # --- HEADER ---
            with ui.row().classes('w-full justify-between items-start max-w-4xl'):
                with ui.column().classes('gap-0'):
                    ui.label(f'ROOM #{room.room_id}').classes('text-2xl font-black text-white').style('-webkit-text-stroke: 2px black;')
                    ui.label(f'{len(room.users)} HUNGRY PEOPLE').classes('text-xs font-bold bg-white border-2 border-black px-2')

                # Avatar List
                with ui.row().classes('gap-[-5px]'):
                    for u in room.users.values():
                        # Overlapping circles
                        with ui.element('div').classes('w-10 h-10 rounded-full border-2 border-black flex items-center justify-center -ml-2 transition hover:scale-125 z-0 hover:z-10 bg-white'):
                            ui.label(u.nickname[0].upper()).classes('font-bold').style(f'color: {u.color}')

            # --- THE CARD TABLE (Messy Grid) ---
            # Flex container allows wrapping, but margins and rotation make it look messy
            with ui.row().classes('w-full max-w-5xl justify-center mt-12 gap-6 p-4 relative'):
                
                if not room.all_cards:
                    with ui.column().classes('items-center opacity-50 mt-10'):
                        ui.label('TABLE IS EMPTY').classes('text-xl')
                        ui.label('Throw some ideas down!').classes('text-sm')

                for card in room.all_cards:
                    is_mine = (card.owner_id == user.uid)
                    
                    # Determine display content
                    # If it's my card -> Show Content
                    # If it's not mine -> Show Pattern (Back) unless flipped
                    
                    # CSS Wrapper for Layout + Entrance Animation
                    # Only animate on first render to prevent re-animation on refresh
                    animation_class = 'card-entry' if not card.has_animated else 'card-entry-done'
                    
                    # Mark as animated after animation starts (use timer to avoid immediate marking)
                    if not card.has_animated:
                        def mark_animated_delayed():
                            card.has_animated = True
                        # Delay marking to ensure animation has time to start
                        ui.timer(0.1, mark_animated_delayed, once=True)
                    
                    # Wrapper with animation - rotation is handled by CSS animation
                    with ui.element('div').classes(animation_class).style(f'--target-rotation: {card.rotation}deg'):
                        
                        # The Card Object itself - rotation will be applied after animation
                        card_element = ui.element('div').classes('messy-card group')
                        
                        # Add click handler for flipping other people's cards
                        if not is_mine:
                            card_element.on('click', lambda c=card: flip_card(c))
                        
                        with card_element:
                            
                            # Delete Button (Only Mine)
                            if is_mine:
                                ui.icon('cancel', size='xs').classes('absolute -top-3 -right-3 bg-red-500 text-white rounded-full p-1 border-2 border-black z-20 cursor-pointer hover:scale-110') \
                                    .on('click', lambda c=card: delete_card(c))

                            # Card Face
                            if is_mine or card.is_flipped:
                                # MY CARD (Face Up) or FLIPPED CARD
                                with ui.element('div').classes('card-content'):
                                    ui.label(card.content).classes('font-bold text-lg leading-tight')
                                    if is_mine:
                                        ui.label('MY PICK').classes('text-[10px] bg-black text-white px-1 absolute bottom-2')
                                    else:
                                        owner_user = room.users.get(card.owner_id)
                                        if owner_user:
                                            ui.label(f'{owner_user.nickname}\'s').classes('text-[10px] bg-black text-white px-1 absolute bottom-2')
                            else:
                                # OTHER CARD (Face Down)
                                # Use card owner's color for the back
                                with ui.element('div').classes('card-content card-back-pattern rounded-lg w-full h-full') \
                                     .style(f'background-color: {card.color};'):
                                    ui.label(card.back_text).classes('text-sm font-bold opacity-80 rotate-[-10deg]')

            # --- FOOTER CONTROLS ---
            with ui.column().classes('fixed bottom-6 left-1/2 transform -translate-x-1/2 items-center gap-2 z-50'):
                # 箭头提示（始终显示）
                if not room.winner_card:
                    with ui.element('div').classes('arrow-tooltip-container'):
                        ui.label('在此输入想吃的餐厅').classes('tooltip-text')
                        ui.label('↓').classes('arrow-down')
                
                with ui.row().classes('bg-white border-[3px] border-black p-2 rounded-xl shadow-[6px_6px_0_rgba(0,0,0,0.3)] gap-2 items-center'):
                    if not room.winner_card:
                        ui.input(placeholder='Sushi? Tacos?').bind_value(input_state, 'text').props('input-class="comic-input"').classes('w-48').on('keydown.enter', add_card)
                        ui.button('ADD', on_click=add_card).classes('funky-btn btn-blue font-bold rounded-lg')
                        
                        if user.uid == room.host_id:
                            ui.element('div').classes('w-[2px] h-8 bg-gray-300 mx-1')
                            ui.button('SPIN!', on_click=start_lottery).classes('funky-btn btn-pink font-black rounded-lg animate-bounce')
                    else:
                        if user.uid == room.host_id:
                            ui.button('RESET TABLE', on_click=reset_game).classes('funky-btn btn-yellow font-bold')

        # --- LOTTERY OVERLAY (SLOT MACHINE) ---
        # Only visible when rolling OR when there is a winner (and user hasn't closed it)
        if room.is_rolling or (room.winner_card and user.uid not in room.overlay_closed_by):
            with ui.element('div').classes('fixed top-0 left-0 w-full h-full slot-machine-overlay flex flex-col items-center justify-center z-[9999]'):
                
                if room.is_rolling:
                    # SPINNING ANIMATION
                    ui.label('ROLLING...').classes('text-white text-xl font-bold mb-4 animate-pulse')
                    # The changing text
                    ui.label(room.current_roll_text).classes('slot-text text-[#ffeaa7] rotate-[-5deg]')
                
                elif room.winner_card:
                    # WINNER REVEAL
                    with ui.column().classes('items-center winner-bounce'):
                        ui.label('WE ARE EATING:').classes('text-white text-lg font-bold mb-4 bg-black px-4 py-1 -rotate-2')
                        
                        # Big Card Display
                        with ui.card().classes('w-64 h-80 bg-white border-[6px] border-[#00b894] items-center justify-center shadow-[0_0_50px_#00b894]'):
                            ui.label(room.winner_card.content).classes('text-4xl font-black text-center leading-tight break-words')
                            
                            winner_user = room.users.get(room.winner_card.owner_id)
                            if winner_user:
                                with ui.row().classes('absolute bottom-4 items-center bg-gray-100 rounded-full px-3 py-1 border border-black'):
                                    ui.label('👑').classes('mr-1')
                                    ui.label(winner_user.nickname).classes('font-bold text-xs')

                    # Action buttons after lottery
                    def close_overlay():
                        """Close the overlay for non-host users (just hide it for this user)"""
                        room.overlay_closed_by.add(user.uid)
                        room.touch()
                    
                    # Only show overlay if user hasn't closed it
                    if user.uid not in room.overlay_closed_by:
                        with ui.row().classes('mt-10 gap-4 items-center'):
                            if user.uid == room.host_id:
                                # Host can restart lottery or reset table
                                ui.button('重新抽奖', on_click=restart_lottery).classes('funky-btn btn-pink font-bold')
                                ui.button('重置桌子', on_click=reset_game).classes('funky-btn btn-yellow font-bold')
                            else:
                                # Non-host can go back to room
                                ui.button('回到房间', on_click=close_overlay).classes('funky-btn btn-blue font-bold')

    # --- POLLING & LOTTERY TIMER ---
    # Fast polling to make the slot machine feel responsive
    last_ts = None
    async def poll():
        nonlocal last_ts
        # If lottery is rolling, poll fast!
        if room.is_rolling or last_ts != room.last_update:
            last_ts = room.last_update
            render_table.refresh()
    
    # Lottery animation timer - updates every 0.05s when rolling
    def lottery_timer():
        if room.is_rolling:
            update_lottery()
        # Also do regular polling
        poll()

    render_table()
    # 0.05s timer for lottery animation (fast updates)
    ui.timer(0.05, lottery_timer)
    # 0.2s polling for general UI updates  
    ui.timer(0.2, poll)

# ==============================================================================
# 4. RUN
# ==============================================================================
ui.run(storage_secret='pixel-picnic-secret', title='Pixel Picnic', favicon='🍔')
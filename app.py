from flask import Flask, render_template, jsonify, request, session
import json, random, os, time
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'learnvest2026secretkey')

# ── GAME DATA ──────────────────────────────────────────────────────────────────

LESSONS = [
    {
        "id": 1, "title": "What is Money?", "icon": "💰", "xp": 20, "coins": 10,
        "age_group": "all", "completed": False,
        "cards": [
            {"title": "Money is a Medium of Exchange", "points": ["Money lets us trade goods and services without bartering", "It has three roles: medium of exchange, store of value, unit of account", "India uses the Indian Rupee (₹) as its official currency", "The RBI (Reserve Bank of India) controls our money supply"]},
            {"title": "Real Indian Example", "story": "Riya earns ₹5,000 pocket money per month. She uses it to buy stationery, food, and saves some for a new phone. Without money, she'd have to barter her old books for lunch!"},
            {"title": "Did You Know? 🤔", "fact": "India has over 1.4 billion people and processes crores of digital transactions every single day through UPI!"}
        ],
        "quiz": [
            {"q": "What does RBI stand for?", "options": ["Reserve Bank of India", "Royal Bank of India", "Rural Bank of India", "Retail Bank of India"], "answer": 0},
            {"q": "Which of these is NOT a function of money?", "options": ["Medium of exchange", "Store of value", "Growing crops", "Unit of account"], "answer": 2},
            {"q": "India's currency symbol is:", "options": ["$", "£", "₹", "€"], "answer": 2}
        ]
    },
    {
        "id": 2, "title": "Saving vs Spending", "icon": "🏦", "xp": 20, "coins": 10,
        "age_group": "all", "completed": False,
        "cards": [
            {"title": "The Golden Rule of Money", "points": ["Always spend LESS than you earn", "The difference between income and expenses is your savings", "Even saving ₹100/day = ₹36,500 in a year!", "Start saving early — time is your biggest asset"]},
            {"title": "Riya's Money Challenge", "story": "Riya earns ₹10,000/month. She spends ₹7,500 on needs and wants. That means she saves ₹2,500 every month. In one year she has ₹30,000 saved — enough for a laptop!"},
            {"title": "Did You Know? 🤔", "fact": "If you save ₹500/month starting at age 18, and it grows at 8% annual interest, you'll have over ₹15 lakhs by age 40!"}
        ],
        "quiz": [
            {"q": "If you earn ₹10,000 and spend ₹7,500, what is your savings rate?", "options": ["25%", "75%", "10%", "50%"], "answer": 0},
            {"q": "Which habit builds wealth faster?", "options": ["Spend first, save what's left", "Save first, spend what's left", "Borrow and invest", "Only spend on needs"], "answer": 1},
            {"q": "Saving ₹500/month for 12 months gives you:", "options": ["₹500", "₹5,000", "₹6,000", "₹12,000"], "answer": 2}
        ]
    },
    {
        "id": 3, "title": "Budgeting Basics", "icon": "📊", "xp": 25, "coins": 15,
        "age_group": "all", "completed": False,
        "cards": [
            {"title": "The 50/30/20 Rule", "points": ["50% of income → NEEDS (rent, food, utilities)", "30% of income → WANTS (entertainment, dining out)", "20% of income → SAVINGS & investments", "This rule works for any income level!"]},
            {"title": "Arjun's Monthly Budget", "story": "Arjun earns ₹20,000/month. Using 50/30/20: ₹10,000 for needs (hostel + food), ₹6,000 for wants (movies + shopping), ₹4,000 goes straight to savings. Simple and powerful!"},
            {"title": "Did You Know? 🤔", "fact": "A written budget can help you save 20% more money than people who don't track expenses. Even a notes app works!"}
        ],
        "quiz": [
            {"q": "In the 50/30/20 rule, what percentage goes to WANTS?", "options": ["50%", "20%", "30%", "10%"], "answer": 2},
            {"q": "Monthly income ₹15,000. How much should go to savings using 50/30/20?", "options": ["₹7,500", "₹4,500", "₹3,000", "₹2,000"], "answer": 2},
            {"q": "Which is a NEED, not a WANT?", "options": ["Netflix subscription", "New iPhone", "Monthly rent", "Weekend trip"], "answer": 2}
        ]
    },
    {
        "id": 4, "title": "Banking & Interest", "icon": "🏛️", "xp": 25, "coins": 15,
        "age_group": "14+", "completed": False,
        "cards": [
            {"title": "How Banks Make Your Money Grow", "points": ["Banks pay you INTEREST for keeping money with them", "Simple Interest: Principal × Rate × Time / 100", "Compound Interest earns interest ON your interest", "FDs (Fixed Deposits) offer 6-8% returns in India"]},
            {"title": "The Magic of Compound Interest", "story": "Priya puts ₹10,000 in an FD at 7% compound interest. After 10 years she has ₹19,671 — almost double! She didn't do any extra work. Her money worked for her."},
            {"title": "Did You Know? 🤔", "fact": "Einstein called compound interest the 8th wonder of the world. He said: 'He who understands it, earns it. He who doesn't, pays it.'"}
        ],
        "quiz": [
            {"q": "Simple Interest on ₹1,000 at 10% for 2 years is:", "options": ["₹100", "₹200", "₹210", "₹1,200"], "answer": 1},
            {"q": "Which grows faster over time?", "options": ["Simple Interest", "Compound Interest", "Both are equal", "Neither grows money"], "answer": 1},
            {"q": "FD stands for:", "options": ["Final Deposit", "Fixed Deposit", "Frequent Deposit", "Flexible Deposit"], "answer": 1}
        ]
    },
    {
        "id": 5, "title": "Stock Market Basics", "icon": "📈", "xp": 30, "coins": 20,
        "age_group": "14+", "completed": False,
        "cards": [
            {"title": "What is the Stock Market?", "points": ["Stocks = tiny ownership pieces of a company", "BSE and NSE are India's two main stock exchanges", "Stock prices go up when company does well, down when it struggles", "Long-term investing historically beats inflation in India"]},
            {"title": "Rahul Invests in Reliance", "story": "Rahul buys 10 shares of Reliance at ₹2,300 each (total ₹23,000). A year later, shares are ₹2,700 each. His investment is now worth ₹27,000 — a ₹4,000 profit, or 17% return!"},
            {"title": "Did You Know? 🤔", "fact": "India's stock market (BSE) is Asia's oldest stock exchange, founded in 1875. Today, over 5,000 companies are listed on Indian exchanges!"}
        ],
        "quiz": [
            {"q": "BSE stands for:", "options": ["Bombay Stock Exchange", "Bank Securities Exchange", "Business Stock Exchange", "Bombay Shares Exchange"], "answer": 0},
            {"q": "If you own stocks in a company, you are a:", "options": ["Debtor", "Creditor", "Shareholder", "Director"], "answer": 2},
            {"q": "Stock prices generally rise when:", "options": ["Company loses money", "Company earns more profits", "Taxes increase", "RBI raises rates"], "answer": 1}
        ]
    },
    {
        "id": 6, "title": "Credit & Loans", "icon": "💳", "xp": 30, "coins": 20,
        "age_group": "18+", "completed": False,
        "cards": [
            {"title": "Understanding Credit", "points": ["Credit = borrowing money you promise to repay later", "Credit Score (300-900): higher is better", "750+ score = great loan rates from banks", "Missing payments damages your credit score significantly"]},
            {"title": "Neha's Credit Card Trap", "story": "Neha spends ₹20,000 on her credit card but only pays the minimum ₹500. The bank charges 36% annual interest! After a year she owes ₹27,200 — she paid ₹6,000 in interest and barely reduced her debt!"},
            {"title": "Did You Know? 🤔", "fact": "India's CIBIL score system grades your creditworthiness from 300-900. A score above 750 can help you get home loans, car loans, and credit cards at lower interest rates!"}
        ],
        "quiz": [
            {"q": "A good CIBIL credit score in India is:", "options": ["300-400", "400-550", "550-700", "750-900"], "answer": 3},
            {"q": "What happens if you miss EMI payments?", "options": ["Nothing happens", "You get a discount", "Your credit score drops", "Bank pays you back"], "answer": 2},
            {"q": "EMI stands for:", "options": ["Equal Monthly Instalment", "Extra Money Income", "Early Money Investment", "Estimated Monthly Interest"], "answer": 0}
        ]
    },
    {
        "id": 7, "title": "Investing Strategies", "icon": "🎯", "xp": 35, "coins": 25,
        "age_group": "18+", "completed": False,
        "cards": [
            {"title": "SIP — India's Favourite Investment", "points": ["SIP = Systematic Investment Plan in Mutual Funds", "Invest as little as ₹500/month in diversified funds", "Rupee-cost averaging reduces market timing risk", "SEBI regulates all mutual funds in India for your safety"]},
            {"title": "The SIP Millionaire Formula", "story": "Vikram starts a ₹5,000/month SIP at age 22. At 12% average annual return, by age 42 he has invested ₹12 lakhs but his portfolio is worth ₹49 lakhs! That's the power of SIP + compounding."},
            {"title": "Did You Know? 🤔", "fact": "India's mutual fund industry crossed ₹50 lakh crore (₹50 trillion) in Assets Under Management in 2024, with SIPs contributing over ₹20,000 crore every single month!"}
        ],
        "quiz": [
            {"q": "SIP stands for:", "options": ["Safe Investment Plan", "Systematic Investment Plan", "Smart Income Plan", "Structured Index Plan"], "answer": 1},
            {"q": "Which body regulates mutual funds in India?", "options": ["RBI", "NCFE", "SEBI", "BSE"], "answer": 2},
            {"q": "The minimum SIP investment in most Indian mutual funds is:", "options": ["₹50", "₹100", "₹500", "₹5,000"], "answer": 2}
        ]
    },
    {
        "id": 8, "title": "Taxes & Filing", "icon": "🧾", "xp": 35, "coins": 25,
        "age_group": "18+", "completed": False,
        "cards": [
            {"title": "Income Tax in India", "points": ["Tax is mandatory — everyone earning above ₹2.5L must file ITR", "New regime: 0% up to ₹3L, then slabs up to 30%", "TDS (Tax Deducted at Source) is deducted by your employer", "File ITR by July 31st every year or face penalties"]},
            {"title": "Ananya Files Her First ITR", "story": "Ananya earns ₹6 lakhs as a fresher. Under the new tax regime, she pays 5% on ₹3-6L = ₹15,000 in tax. But she claims HRA deduction and brings it down to ₹8,000. Smart tax planning saved her ₹7,000!"},
            {"title": "Did You Know? 🤔", "fact": "India had over 7.4 crore income tax return filers in 2023-24. Filing your ITR is not just a legal duty — it also builds your financial credibility for loans and visas!"}
        ],
        "quiz": [
            {"q": "Income Tax Return deadline in India is normally:", "options": ["March 31", "July 31", "December 31", "January 31"], "answer": 1},
            {"q": "TDS stands for:", "options": ["Tax Deducted at Source", "Total Deposit System", "Tax Due Settlement", "Term Deposit Scheme"], "answer": 0},
            {"q": "Below what annual income is no tax owed under the new regime?", "options": ["₹1.5 Lakhs", "₹2 Lakhs", "₹3 Lakhs", "₹5 Lakhs"], "answer": 2}
        ]
    }
]

STOCKS = [
    {"symbol": "RLNC", "name": "VestReliance", "base": 2340, "sector": "Energy & Retail"},
    {"symbol": "INFX", "name": "VestInfosys", "base": 1850, "sector": "Technology"},
    {"symbol": "HDFC", "name": "VestHDFC Bank", "base": 1620, "sector": "Banking"},
    {"symbol": "ZMTO", "name": "VestZomato", "base": 210,  "sector": "Food Tech"},
    {"symbol": "TATA", "name": "VestTata Motors", "base": 960, "sector": "Automobile"},
    {"symbol": "WIPX", "name": "VestWipro", "base": 480,  "sector": "Technology"},
]

LIFE_EVENTS = [
    {"id": 1, "title": "🚨 Medical Emergency!", "desc": "Your parent needs urgent treatment costing ₹15,000 VestCoins.", "choices": [
        {"text": "Pay from savings", "effect": -15000, "outcome": "You dipped into savings but handled it. Good emergency fund planning for next time!"},
        {"text": "Take a loan (pay 12% interest)", "effect": -16800, "outcome": "You took a loan. Remember: always keep 3-6 months expenses as emergency fund!"},
        {"text": "Sell some stocks", "effect": -15000, "outcome": "Smart! Liquid assets saved you. Keep some investments in easily accessible funds."}
    ]},
    {"id": 2, "title": "📉 Market Crash!", "desc": "The simulated market just dropped 20%. Your portfolio lost value.", "choices": [
        {"text": "Panic sell everything", "effect": -5000, "outcome": "Selling in panic locks in losses. Markets historically recover. Stay calm!"},
        {"text": "Hold and wait", "effect": 0, "outcome": "Wise decision! Markets recover over time. Long-term investors beat short-term traders."},
        {"text": "Buy more (Buy the dip!)", "effect": 3000, "outcome": "Bold move! Buying during crashes can accelerate wealth. Warren Buffett does this!"}
    ]},
    {"id": 3, "title": "🎉 Diwali Bonus!", "desc": "You received ₹10,000 VestCoins as a bonus. What do you do?", "choices": [
        {"text": "Spend on celebration", "effect": -10000, "outcome": "You celebrated! But what about your future self? Try to save at least 50% of windfalls."},
        {"text": "Put it all in savings", "effect": 10000, "outcome": "Disciplined! Your savings balance grows. Consider investing half for even better returns."},
        {"text": "Invest 70%, celebrate with 30%", "effect": 7000, "outcome": "Perfect balance! ₹7,000 invested + ₹3,000 enjoyed. This is exactly the right mindset!"}
    ]},
    {"id": 4, "title": "💼 Business Opportunity!", "desc": "A chai stall opportunity needs ₹8,000 investment. 60% chance of ₹15,000 return.", "choices": [
        {"text": "Invest all ₹8,000", "effect": random.choice([7000, -8000]), "outcome": "High risk, high reward! Entrepreneurship drives India's economy."},
        {"text": "Pass — too risky", "effect": 0, "outcome": "Conservative but safe. Not all opportunities are worth the risk. Good risk management!"},
        {"text": "Invest ₹4,000 (half risk)", "effect": random.choice([3500, -4000]), "outcome": "Smart diversification! Never put all eggs in one basket."}
    ]},
    {"id": 5, "title": "🏠 Rent Due!", "desc": "Monthly hostel fee of ₹8,000 VestCoins is due. Do you have enough?", "choices": [
        {"text": "Pay from savings", "effect": -8000, "outcome": "Housing is a need — always budget for it first! Shelter before wants."},
        {"text": "Ask parents for help", "effect": -8000, "outcome": "Sometimes we need support. But build an emergency fund to be independent!"},
        {"text": "Negotiate payment plan", "effect": -4000, "outcome": "Resourceful! Communication and negotiation are valuable financial life skills."}
    ]}
]

BUSINESSES = [
    {"id": 1, "name": "Chai Stall ☕", "cost": 5000, "base_revenue": 800, "risk": "low", "desc": "Low investment, steady daily income from students and office workers."},
    {"id": 2, "name": "Mobile Repair Shop 📱", "cost": 15000, "base_revenue": 2200, "risk": "medium", "desc": "Moderate investment with growing demand as smartphone usage rises."},
    {"id": 3, "name": "Online Clothes Store 👗", "cost": 20000, "base_revenue": 3500, "risk": "medium", "desc": "E-commerce is booming in India. Higher growth potential with right marketing."},
    {"id": 4, "name": "Tech Startup 💻", "cost": 50000, "base_revenue": 8000, "risk": "high", "desc": "High risk, high reward. India's startup ecosystem is the world's 3rd largest!"}
]

BADGES = [
    {"id": "first_lesson", "name": "First Step", "icon": "🎓", "desc": "Complete your first lesson", "unlocked": False},
    {"id": "streak_7", "name": "7-Day Streak", "icon": "🔥", "desc": "Learn 7 days in a row", "unlocked": False},
    {"id": "first_invest", "name": "First Investment", "icon": "📈", "desc": "Make your first stock purchase", "unlocked": False},
    {"id": "saver", "name": "Super Saver", "icon": "🏦", "desc": "Save 10,000 VestCoins", "unlocked": False},
    {"id": "entrepreneur", "name": "Entrepreneur", "icon": "🏭", "desc": "Start a virtual business", "unlocked": False},
    {"id": "millionaire", "name": "VestCoin Millionaire", "icon": "💎", "desc": "Accumulate 1,00,000 VestCoins net worth", "unlocked": False},
    {"id": "all_lessons", "name": "Scholar", "icon": "📚", "desc": "Complete all 8 lessons", "unlocked": False},
    {"id": "property", "name": "Property Owner", "icon": "🏠", "desc": "Buy your first virtual property", "unlocked": False},
]

def get_state():
    if 'state' not in session:
        session['state'] = {
            'name': 'Arjun',
            'xp': 0,
            'coins': 2000,
            'streak': 0,
            'savings': 5000,
            'savings_interest': 0.05,
            'portfolio': {},
            'business': None,
            'business_level': 0,
            'properties': [],
            'badges': [b.copy() for b in BADGES],
            'completed_lessons': [],
            'vest_score': 500,
            'week': 1,
            'events_seen': [],
            'stock_history': {s['symbol']: [s['base']] for s in STOCKS}
        }
    return session['state']

def save_state(state):
    session['state'] = state
    session.modified = True

# ── ROUTES ─────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/state')
def api_state():
    return jsonify(get_state())

@app.route('/api/lessons')
def api_lessons():
    state = get_state()
    lessons = []
    for l in LESSONS:
        lc = l.copy()
        lc['completed'] = l['id'] in state['completed_lessons']
        lessons.append(lc)
    return jsonify(lessons)

@app.route('/api/lesson/<int:lid>')
def api_lesson(lid):
    lesson = next((l for l in LESSONS if l['id'] == lid), None)
    if not lesson:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(lesson)

@app.route('/api/complete_lesson', methods=['POST'])
def complete_lesson():
    data = request.json
    lid = data.get('lesson_id')
    score = data.get('score', 0)
    state = get_state()
    lesson = next((l for l in LESSONS if l['id'] == lid), None)
    if not lesson:
        return jsonify({'error': 'Not found'}), 404
    already = lid in state['completed_lessons']
    bonus_xp = int(lesson['xp'] * (score / 3))
    bonus_coins = int(lesson['coins'] * (score / 3))
    if not already:
        state['completed_lessons'].append(lid)
        state['xp'] += lesson['xp'] + bonus_xp
        state['coins'] += lesson['coins'] + bonus_coins
        state['streak'] += 1
        if lid == 1 and not any(b['id'] == 'first_lesson' and b['unlocked'] for b in state['badges']):
            for b in state['badges']:
                if b['id'] == 'first_lesson': b['unlocked'] = True
        if len(state['completed_lessons']) == len(LESSONS):
            for b in state['badges']:
                if b['id'] == 'all_lessons': b['unlocked'] = True
    save_state(state)
    return jsonify({'xp': state['xp'], 'coins': state['coins'], 'streak': state['streak'], 'already_done': already, 'earned_xp': lesson['xp'] + bonus_xp, 'earned_coins': lesson['coins'] + bonus_coins})

@app.route('/api/stocks')
def api_stocks():
    state = get_state()
    result = []
    for s in STOCKS:
        history = state['stock_history'].get(s['symbol'], [s['base']])
        last = history[-1]
        change = round(random.uniform(-4.5, 5.5), 2)
        new_price = max(10, round(last * (1 + change / 100), 2))
        history.append(new_price)
        if len(history) > 14:
            history = history[-14:]
        state['stock_history'][s['symbol']] = history
        owned = state['portfolio'].get(s['symbol'], {}).get('qty', 0)
        avg_price = state['portfolio'].get(s['symbol'], {}).get('avg_price', 0)
        result.append({**s, 'price': new_price, 'change': change, 'history': history, 'owned': owned, 'avg_price': avg_price})
    save_state(state)
    return jsonify(result)

@app.route('/api/buy_stock', methods=['POST'])
def buy_stock():
    data = request.json
    symbol, qty = data.get('symbol'), int(data.get('qty', 1))
    state = get_state()
    stock = next((s for s in STOCKS if s['symbol'] == symbol), None)
    if not stock:
        return jsonify({'error': 'Stock not found'}), 404
    history = state['stock_history'].get(symbol, [stock['base']])
    price = history[-1]
    total = price * qty
    if state['coins'] < total:
        return jsonify({'error': 'Insufficient VestCoins'}), 400
    state['coins'] -= total
    if symbol not in state['portfolio']:
        state['portfolio'][symbol] = {'qty': 0, 'avg_price': 0}
    p = state['portfolio'][symbol]
    total_qty = p['qty'] + qty
    p['avg_price'] = round(((p['qty'] * p['avg_price']) + (qty * price)) / total_qty, 2)
    p['qty'] = total_qty
    for b in state['badges']:
        if b['id'] == 'first_invest': b['unlocked'] = True
    save_state(state)
    return jsonify({'success': True, 'coins': state['coins'], 'portfolio': state['portfolio']})

@app.route('/api/sell_stock', methods=['POST'])
def sell_stock():
    data = request.json
    symbol, qty = data.get('symbol'), int(data.get('qty', 1))
    state = get_state()
    if symbol not in state['portfolio'] or state['portfolio'][symbol]['qty'] < qty:
        return jsonify({'error': 'Not enough shares'}), 400
    history = state['stock_history'].get(symbol, [STOCKS[0]['base']])
    price = history[-1]
    total = price * qty
    state['coins'] += total
    state['portfolio'][symbol]['qty'] -= qty
    if state['portfolio'][symbol]['qty'] == 0:
        del state['portfolio'][symbol]
    save_state(state)
    return jsonify({'success': True, 'coins': state['coins']})

@app.route('/api/deposit', methods=['POST'])
def deposit():
    data = request.json
    amount = int(data.get('amount', 0))
    state = get_state()
    if state['coins'] < amount:
        return jsonify({'error': 'Insufficient coins'}), 400
    state['coins'] -= amount
    state['savings'] += amount
    interest = round(state['savings'] * state['savings_interest'] / 52)
    state['savings'] += interest
    state['savings_interest_earned'] = state.get('savings_interest_earned', 0) + interest
    for b in state['badges']:
        if b['id'] == 'saver' and state['savings'] >= 10000: b['unlocked'] = True
    save_state(state)
    return jsonify({'coins': state['coins'], 'savings': state['savings'], 'interest_earned': interest})

@app.route('/api/withdraw', methods=['POST'])
def withdraw():
    data = request.json
    amount = int(data.get('amount', 0))
    state = get_state()
    if state['savings'] < amount:
        return jsonify({'error': 'Insufficient savings'}), 400
    state['savings'] -= amount
    state['coins'] += amount
    save_state(state)
    return jsonify({'coins': state['coins'], 'savings': state['savings']})

@app.route('/api/start_business', methods=['POST'])
def start_business():
    data = request.json
    bid = int(data.get('business_id'))
    state = get_state()
    biz = next((b for b in BUSINESSES if b['id'] == bid), None)
    if not biz:
        return jsonify({'error': 'Not found'}), 404
    if state['coins'] < biz['cost']:
        return jsonify({'error': 'Insufficient coins'}), 400
    state['coins'] -= biz['cost']
    state['business'] = biz.copy()
    state['business']['revenue'] = biz['base_revenue']
    state['business']['expenses'] = int(biz['base_revenue'] * 0.4)
    state['business']['level'] = 1
    state['business']['weeks_running'] = 0
    for b in state['badges']:
        if b['id'] == 'entrepreneur': b['unlocked'] = True
    save_state(state)
    return jsonify({'success': True, 'business': state['business'], 'coins': state['coins']})

@app.route('/api/business_tick', methods=['POST'])
def business_tick():
    state = get_state()
    if not state.get('business'):
        return jsonify({'error': 'No business'}), 400
    biz = state['business']
    variance = random.uniform(0.85, 1.20)
    profit = int((biz['revenue'] - biz['expenses']) * variance)
    state['coins'] += max(0, profit)
    biz['weeks_running'] = biz.get('weeks_running', 0) + 1
    if biz['weeks_running'] % 4 == 0:
        biz['revenue'] = int(biz['revenue'] * 1.05)
    save_state(state)
    return jsonify({'profit': profit, 'coins': state['coins'], 'business': biz})

@app.route('/api/buy_property', methods=['POST'])
def buy_property():
    data = request.json
    ptype = data.get('type', '1bhk')
    prices = {'studio': 50000, '1bhk': 80000, '2bhk': 150000, 'villa': 300000}
    names = {'studio': 'Studio Apartment 🏢', '1bhk': '1BHK Flat 🏠', '2bhk': '2BHK Apartment 🏡', 'villa': 'Villa 🏰'}
    price = prices.get(ptype, 80000)
    state = get_state()
    if state['coins'] < price:
        return jsonify({'error': 'Insufficient coins'}), 400
    state['coins'] -= price
    state['properties'].append({'type': ptype, 'name': names[ptype], 'value': price, 'rent': int(price * 0.005)})
    for b in state['badges']:
        if b['id'] == 'property': b['unlocked'] = True
    save_state(state)
    return jsonify({'success': True, 'properties': state['properties'], 'coins': state['coins']})

@app.route('/api/life_event')
def life_event():
    state = get_state()
    unseen = [e for e in LIFE_EVENTS if e['id'] not in state.get('events_seen', [])]
    if not unseen:
        state['events_seen'] = []
        unseen = LIFE_EVENTS
    event = random.choice(unseen)
    save_state(state)
    return jsonify(event)

@app.route('/api/resolve_event', methods=['POST'])
def resolve_event():
    data = request.json
    event_id = data.get('event_id')
    choice_idx = data.get('choice_idx', 0)
    state = get_state()
    event = next((e for e in LIFE_EVENTS if e['id'] == event_id), None)
    if not event:
        return jsonify({'error': 'Not found'}), 404
    choice = event['choices'][choice_idx]
    effect = choice['effect']
    if effect > 0:
        state['coins'] += effect
    else:
        state['coins'] = max(0, state['coins'] + effect)
    if event_id not in state['events_seen']:
        state['events_seen'].append(event_id)
    net_worth = state['coins'] + state['savings'] + sum(p['value'] for p in state.get('properties', []))
    for b in state['badges']:
        if b['id'] == 'millionaire' and net_worth >= 100000: b['unlocked'] = True
    save_state(state)
    return jsonify({'outcome': choice['outcome'], 'effect': effect, 'coins': state['coins']})

@app.route('/api/leaderboard')
def leaderboard():
    state = get_state()
    others = [
        {'name': 'Priya Sharma', 'xp': 1840, 'streak': 12, 'avatar': 'P'},
        {'name': 'Rahul Verma', 'xp': 1620, 'streak': 8, 'avatar': 'R'},
        {'name': 'Ananya Singh', 'xp': 1450, 'streak': 15, 'avatar': 'A'},
        {'name': 'Rohan Mehta', 'xp': 1200, 'streak': 5, 'avatar': 'M'},
        {'name': 'Sneha Patel', 'xp': 980, 'streak': 3, 'avatar': 'S'},
    ]
    all_users = others + [{'name': state['name'] + ' (You)', 'xp': state['xp'], 'streak': state['streak'], 'avatar': state['name'][0].upper(), 'is_me': True}]
    all_users.sort(key=lambda x: x['xp'], reverse=True)
    for i, u in enumerate(all_users):
        u['rank'] = i + 1
    return jsonify(all_users)

@app.route('/api/set_name', methods=['POST'])
def set_name():
    data = request.json
    state = get_state()
    state['name'] = data.get('name', 'Student')
    save_state(state)
    return jsonify({'success': True})

@app.route('/api/reset', methods=['POST'])
def reset():
    session.clear()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

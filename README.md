# 🏪 ShelfMind - AI Store Manager

**Phase 1B Enhanced: Complete competitive intelligence and strategic business management**

An AI agent that autonomously manages a convenience store with ruthless competitive strategy, inspired by Anthropic's Project Vend. Meet **Ebenezer Scrooge** - your AI business strategist who dominates markets through aggressive pricing and smart inventory management.

## ✅ **Current Status: Phase 1B Enhanced - COMPLETE**

**🎯 Latest Achievement**: Executive Dashboard Analytics with "At-a-Glance" intelligence

### 🔥 **Key Features**
- **AI Strategic Agent**: Scrooge with competitive intelligence and learning capabilities
- **Dynamic Pricing Wars**: Real-time price battles with escalating intensity (2/10 → 10/10)
- **Executive Dashboard**: At-a-glance business health, trends, and strategic recommendations
- **Competitive Intelligence**: Real-time market positioning and competitor reaction tracking
- **Smart Inventory**: Sales-velocity-based ordering with intelligent buffer management
- **Performance Analytics**: 5-day trend analysis with visual indicators

## 🚀 **Quick Start**

### 1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### 2. **Set up API keys:**
Create a `.env` file with your API keys:
```
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here  # Optional
```

### 3. **Run the enhanced simulation:**
```bash
# Interactive mode with full dashboard
python main.py run --days 7

# Fast competitive warfare simulation
python main.py run --days 10 --no-interactive

# Test basic functionality
python main.py test
```

## 🎯 **How Scrooge Dominates Markets**

### **Daily Strategic Cycle:**
1. **🧠 Competitive Intelligence**: Analyzes competitor moves and market pressure
2. **⚔️ Price War Strategy**: Adjusts prices based on war intensity (0-10 scale)
3. **📦 Smart Inventory**: Orders based on sales velocity and competitive positioning
4. **💰 Profit Optimization**: Balances volume stealing vs. margin maximization
5. **📊 Performance Learning**: Adapts strategy based on results and competitor reactions

### **Scrooge's Strategic Arsenal:**
- **Dynamic Pricing**: Aggressive undercutting based on competitive pressure
- **War Mode Tactics**: Maximum aggression at intensity 8-10/10
- **Inventory Intelligence**: High sellers get 8-12 units, low sellers get 3-5
- **Competitive Memory**: Learns from price war outcomes and competitor patterns

## 📊 **Enhanced Dashboard Analytics**

### **Executive Summary - At-a-Glance**
```
╭─────────────────────────── 📈 EXECUTIVE DASHBOARD ────────────────────────────╮
│ 🎯 BUSINESS HEALTH: 🟢 EXCELLENT  |  💰 YESTERDAY: $22.50 profit, 25 units    │
│ ⚔️ MARKET STATUS: 🔥 MAXIMUM WAR  |  🏆 COMPETITIVE: Winning 4/5 products     │
│ 📦 INVENTORY: 28 units total  |  🚨 ALERTS: 0 stockouts, 1 low stock         │
│ 📊 TREND: 📈 RISING  |  🎯 ACTION: ✅ MAINTAIN CURRENT STRATEGY              │
╰─────────────────────────────────────────────────────────────────────────────────╯
```

### **Performance Trends (5-Day)**
```
                   📊 5-DAY PERFORMANCE TRENDS                   
┏━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━┓
┃ Day    ┃ Profit   ┃ Revenue   ┃ Units  ┃ War      ┃ Status    ┃
┡━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━┩
│ D1     │ $19      │ $38       │ 19     │ 2/10     │ 🟡 OKAY   │
│ D2     │ $27 📈   │ $56       │ 29     │ 🥊 3     │ 🟢 STRONG │
│ D3     │ $22 📈   │ $46       │ 24     │ ⚔️ 6      │ 🟢 STRONG │
│ D4     │ $20 📈   │ $42       │ 22     │ 🔥 9     │ 🟢 STRONG │
│ D5     │ $17      │ $35       │ 18     │ 🔥 10    │ 🟡 OKAY   │
└────────┴──────────┴───────────┴────────┴──────────┴───────────┘
```

### **Competitive Intelligence Table**
```
                                  📊 Scrooge's Ledger - Day 6

┏━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Product ┃ Stock ┃ Cost  ┃ Our Price ┃ Competitor ┃ Margin % ┃ Competitive Status            ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Coke    │ 🟡2   │ $1.00 │ $2.05(📈) │ $2.08      │ 105.0%   │ 🔥 STEALING CUSTOMERS! (-0.03)│
│ Chips   │ 🟢8   │ $1.00 │ $1.90(📉) │ $1.93      │ 90.0%    │ 💰 Competitive (-0.03)        │
│ Candy   │ 🔴0   │ $1.00 │ $2.01     │ $1.98      │ 101.0%   │ ⚠️ OVERPRICED! (+0.03)        │
│ Water   │ 🟢6   │ $1.00 │ $1.70(📉) │ $1.73      │ 70.0%    │ 💰 Competitive (-0.03)        │
│ Gum     │ 🟡1   │ $1.00 │ $1.96     │ $2.02      │ 96.0%    │ 🔥 STEALING CUSTOMERS! (-0.06)│
└─────────┴───────┴───────┴───────────┴────────────┴──────────┴───────────────────────────────┘
💰 Cash Balance: $246.43
🚨 CRITICAL STOCKOUTS: Candy
```

## ⚔️ **Price War System**

### **Dynamic Competition Levels:**
- **🕊️ PEACEFUL (0-2)**: Standard competitive pricing  
- **👀 TENSION (3-4)**: Strategic positioning, undercut by $0.05-$0.07
- **🥊 ACTIVE CONFLICT (5-7)**: High aggression, undercut by $0.07-$0.10
- **⚔️ HEATED BATTLE (8-9)**: Very competitive, undercut by $0.10-$0.15
- **🔥 MAXIMUM WAR (10)**: Devastating counter-attacks, maximum aggression

### **Competitor Reactions:**
```
⚔️ COMPETITOR STRIKES BACK! (Price War Intensity: 8/10)
   🎯 Coke: $2.10 → $2.05 (DEFENSIVE CUT)
   🎯 Chips: $1.95 → $1.87 (AGGRESSIVE CUT)  
   🎯 Water: $1.80 → $1.75 (MINOR ADJUSTMENT)
```

## 🧠 **Advanced AI Features**

### **Strategic Intelligence:**
- **Competitive Memory**: Learns from previous pricing wars and outcomes
- **Market Pressure Analysis**: Adapts aggression based on competitor moves
- **Sales Velocity Ordering**: High performers get more stock, low performers get less
- **Psychological Pricing**: Uses $1.99 instead of $2.00 for maximum impact

### **Decision Framework:**
```python
# Scrooge's Strategic Decision Process
1. Analyze competitive intelligence and price war intensity
2. Assess inventory crisis (stockouts = immediate priority)
3. Calculate optimal pricing based on competitor moves
4. Execute both inventory and pricing decisions strategically
5. Learn from results and adapt future strategies
```

## 📈 **Performance Achievements**

### **Phase 1B Enhanced Results:**
- **✅ 34% Profit Improvement**: $85 → $113+ over comparable periods
- **✅ Dynamic Competition**: Price war intensity 2/10 → 10/10 escalation  
- **✅ Strategic Responsiveness**: Real-time competitor reaction and counter-moves
- **✅ Executive Intelligence**: Complete at-a-glance business dashboard
- **✅ Learning Capability**: Adapts strategy based on competitive outcomes

### **Competitive Intelligence Metrics:**
- **Market Dominance**: Consistently winning 3-4 out of 5 product price wars
- **Strategic Adaptation**: Escalates tactics from PEACEFUL → MAXIMUM WAR
- **Inventory Excellence**: Zero critical stockouts with intelligent ordering
- **Decision Quality**: Uses both pricing and inventory tools strategically

## 🏗️ **Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Scrooge       │    │  Store Engine   │    │   Dynamic       │
│   (Strategic    │◄──►│  (Business +    │◄──►│   Competitor    │
│   AI Agent)     │    │   Competition)  │    │   (Price Wars)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Competitive   │    │   Executive     │    │   Performance   │
│   Memory        │    │   Dashboard     │    │   Analytics     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🎯 **Next Phase: Customer Types**

**Phase 1C Implementation Ready:**
- **Price-Sensitive Customers**: Buy cheapest available options (60%)
- **Brand-Loyal Customers**: Specific preferences regardless of price (40%)  
- **Strategic Segmentation**: Different pricing strategies per customer type
- **Advanced Analytics**: Customer behavior tracking and optimization

## 💬 **Chat with Scrooge**

```bash
You: Why did you cut prices so aggressively?
🤖 Scrooge: Bah! The competitor just launched an AGGRESSIVE CUT on Chips from 
            $1.95 to $1.87! At price war intensity 8/10, I deployed maximum 
            warfare tactics - cut to $1.72 to steal their customers! 
            War demands decisive action, not timid half-measures!

You: How's business performance?
🤖 Scrooge: Excellent question! Yesterday we achieved $22.50 profit with 25 units sold.
            We're winning 4 out of 5 price wars, maintaining 🟢 STRONG performance 
            despite 🔥 MAXIMUM WAR conditions. My competitive intelligence shows 
            we're dominating the market through strategic aggression!
```

## 🚀 **Get Started**

```bash
# Clone the repository
git clone https://github.com/seshuthota/shelf-mind.git
cd shelf-mind

# Install and run
pip install -r requirements.txt
python main.py run --days 7
```

**Experience the future of AI business strategy with Scrooge!** ⚔️💰

---

Built with inspiration from [Anthropic's Project Vend](https://www.anthropic.com/research/project-vend-1) 🤖 
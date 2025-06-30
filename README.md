# 🏪 Claudius - AI Store Manager

An AI agent that autonomously manages a convenience store, inspired by Anthropic's Project Vend.

## Phase 1A: Ultra-Basic Store

**Current Features:**
- 5 products (Coke, Chips, Candy, Water, Gum)
- Simple customer simulation (10-20 customers/day buying 1-3 random items)
- LLM agent (Claudius) makes daily ordering decisions
- Basic inventory and cash management
- Interactive CLI with store dashboard

## Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up API keys:**
Create a `.env` file with your API keys:
```
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here
```

3. **Test the system:**
```bash
python main.py test
```

4. **Run the simulation:**
```bash
# Interactive mode (default)
python main.py run

# Fast mode for 30 days
python main.py run --days 30 --no-interactive
```

## How It Works

**Daily Cycle:**
1. Claudius analyzes store status (inventory, cash, yesterday's sales)
2. Makes ordering decisions using LLM reasoning
3. Customers visit and make purchases
4. End of day summary shows profit/loss

**Claudius's Goal:** Avoid stockouts while maximizing profit

**Example Decision Making:**
- "I see Coke is down to 2 units and sold 8 yesterday, I should order 10 more"
- "Cash is low at $15, I'll only order the most critical items"
- "Gum didn't sell well, I'll order less this time"

## Phase 1A Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Claudius      │    │  Store Engine   │    │   Customers     │
│   (LLM Agent)   │◄──►│  (Business      │◄──►│  (Random        │
│                 │    │   Logic)        │    │   Simulation)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│   Memory        │    │   Dashboard     │
│   (Decisions)   │    │   (CLI)         │
└─────────────────┘    └─────────────────┘
```

## Example Output

```
📊 Store Status - Day 1
┌─────────┬──────────┬────────┬────────┬────────┐
│ Product │ In Stock │ Cost   │ Price  │ Status │
├─────────┼──────────┼────────┼────────┼────────┤
│ Coke    │ 10       │ $1.00  │ $2.00  │ 🟢     │
│ Chips   │ 10       │ $1.00  │ $2.00  │ 🟢     │
│ Candy   │ 10       │ $1.00  │ $2.00  │ 🟢     │
│ Water   │ 10       │ $1.00  │ $2.00  │ 🟢     │
│ Gum     │ 10       │ $1.00  │ $2.00  │ 🟢     │
└─────────┴──────────┴────────┴────────┴────────┘
💰 Cash Balance: $100.00

🤖 Claudius decided to order: {'Coke': 5, 'Chips': 3}
🛒 15 customers visited today

╭─────── Day 1 Summary ───────╮
│ 💰 Revenue: $28.00          │
│ 📈 Profit: $14.00           │
│ 🛒 Units Sold: 14           │
│ 💵 Cash Balance: $122.00    │
│ 📦 Inventory: {...}         │
╰─────────────────────────────╯
```

## Success Metrics (Phase 1A)

- ✅ **Basic Goal**: Claudius avoids stockouts and makes profit for 7 days
- ✅ **Learning**: Shows different ordering patterns based on sales data
- ✅ **Safety**: Never overspends available cash
- ✅ **Reasoning**: Provides explanations for decisions

## Next Phases

- **Phase 1B**: Add pricing decisions and price sensitivity
- **Phase 1C**: Multiple customer types (price-sensitive vs brand-loyal)
- **Phase 1D**: Multiple suppliers with different terms
- **Phase 2**: Market dynamics and competition

## Chat with Claudius

```bash
You: Why did you order so much Coke?
🤖 Claudius: I noticed Coke sold 8 units yesterday but we only had 2 left. 
             With 15+ customers expected today, I ordered 10 to avoid 
             stockouts while maintaining good profit margins.
```

Built with inspiration from [Anthropic's Project Vend](https://www.anthropic.com/research/project-vend-1) 🤖 
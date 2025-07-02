import random
from typing import Dict, List
from src.core.models import PRODUCTS


class CompetitorEngine:
    """🔥 Phase 1B Enhanced: ULTRA-AGGRESSIVE Competition System 🔥"""
    
    def __init__(self):
        # Phase 2A Enhanced: ULTRA-AGGRESSIVE Competition System - 10 Products!
        # Initialize competitor prices slightly different from our defaults for each product
        base_prices = {
            "Coke": 2.10, "Water": 1.80, "Chips": 1.95, "Crackers": 1.85,
            "Sandwiches": 4.20, "Bananas": 1.15, "Ice Cream": 3.40,
            "Candy": 2.20, "Gum": 2.05, "Chocolate": 2.50
        }
        self.competitor_prices = base_prices
        
        # Enhanced competitor intelligence and aggression tracking
        self.competitor_last_prices = self.competitor_prices.copy()
        self.price_war_intensity = 0  # 0-10 scale of how vicious the war is
        self.competitor_reactions = []
        self.competitor_strategy = "BALANCED"  # Changes daily: AGGRESSIVE, DEFENSIVE, PREDATORY, PSYCHOLOGICAL
        self.competitor_cash_reserves = 500.0  # Competitor has deep pockets
        self.days_since_last_attack = 0  # Tracks when competitor last initiated
        self.our_total_undercuts = 0  # Tracks how much we've been undercutting
        self.competitor_revenge_mode = False  # Special mode when competitor gets really pissed
    
    def update_competitor_prices(self, current_prices: Dict[str, float], day: int) -> List[str]:
        """🔥 ULTRA-AGGRESSIVE competitor that will make Scrooge sweat bullets! 🔥"""
        reactions = []
        
        # Update competitor's daily strategy - they adapt and get nastier
        self._update_competitor_strategy()
        
        # Track our aggressive behavior
        self._track_our_undercuts(current_prices)
        
        # Phase 1: Reactive responses to our moves
        reactive_moves = self._execute_reactive_strategy(current_prices)
        reactions.extend(reactive_moves)
        
        # Phase 2: Proactive attacks (competitor initiates fights!)
        proactive_moves = self._execute_proactive_strategy(current_prices)
        reactions.extend(proactive_moves)
        
        # Phase 3: Psychological warfare and dirty tactics
        psychological_moves = self._execute_psychological_warfare()
        reactions.extend(psychological_moves)
        
        # Update war intensity and revenge mode
        self._update_war_dynamics(reactions)
        
        # Store reactions for Scrooge's analysis
        if reactions:
            self.competitor_reactions.append({
                "day": day,
                "reactions": reactions,
                "intensity": self.price_war_intensity,
                "strategy": self.competitor_strategy,
                "revenge_mode": self.competitor_revenge_mode
            })
        
        self.days_since_last_attack += 1
        return reactions
    
    def _update_competitor_strategy(self):
        """Competitor adapts their strategy based on market conditions"""
        strategies = ["AGGRESSIVE", "DEFENSIVE", "PREDATORY", "PSYCHOLOGICAL", "BALANCED"]
        
        # Higher war intensity = more aggressive strategies
        if self.price_war_intensity >= 8:
            self.competitor_strategy = random.choice(["PREDATORY", "PSYCHOLOGICAL", "AGGRESSIVE"])
        elif self.price_war_intensity >= 5:
            self.competitor_strategy = random.choice(["AGGRESSIVE", "PREDATORY", "PSYCHOLOGICAL"])
        elif self.price_war_intensity >= 3:
            self.competitor_strategy = random.choice(["AGGRESSIVE", "BALANCED", "DEFENSIVE"])
        else:
            # Sometimes they randomly get aggressive even when things are calm
            if random.random() < 0.15:  # 15% chance of random aggression
                self.competitor_strategy = "AGGRESSIVE"
            else:
                self.competitor_strategy = random.choice(["BALANCED", "DEFENSIVE"])
    
    def _track_our_undercuts(self, current_prices: Dict[str, float]):
        """Track how much we've been undercutting - builds competitor anger"""
        total_undercuts = 0
        for product_name in PRODUCTS.keys():
            our_price = current_prices[product_name]
            competitor_price = self.competitor_prices[product_name]
            if our_price < competitor_price:
                total_undercuts += (competitor_price - our_price)
        
        self.our_total_undercuts += total_undercuts
        
        # Trigger revenge mode if we've been too aggressive
        if self.our_total_undercuts > 1.0 and not self.competitor_revenge_mode:
            self.competitor_revenge_mode = True
            
    def _execute_reactive_strategy(self, current_prices: Dict[str, float]) -> List[str]:
        """Competitor reacts to our pricing moves"""
        reactions = []
        
        for product_name in PRODUCTS.keys():
            our_price = current_prices[product_name]
            competitor_price = self.competitor_prices[product_name]
            product_cost = PRODUCTS[product_name].cost
            
            price_difference = competitor_price - our_price
            
            if price_difference <= 0:  # We're not cheaper, skip
                continue
                
            # Calculate reaction intensity based on strategy
            reaction_multiplier = {
                "AGGRESSIVE": 1.2,
                "PREDATORY": 1.5,
                "PSYCHOLOGICAL": 1.0,
                "DEFENSIVE": 0.7,
                "BALANCED": 1.0
            }.get(self.competitor_strategy, 1.0)
            
            # Base reaction chance
            if price_difference > 0.20:
                reaction_chance = 0.95 * reaction_multiplier
                cut_percentage = 0.8  # Cut 80% of difference
            elif price_difference > 0.15:
                reaction_chance = 0.85 * reaction_multiplier
                cut_percentage = 0.7
            elif price_difference > 0.10:
                reaction_chance = 0.70 * reaction_multiplier
                cut_percentage = 0.6
            elif price_difference > 0.05:
                reaction_chance = 0.50 * reaction_multiplier
                cut_percentage = 0.5
            else:
                reaction_chance = 0.25 * reaction_multiplier
                cut_percentage = 0.4
            
            # Revenge mode makes them MUCH more aggressive
            if self.competitor_revenge_mode:
                reaction_chance = min(0.98, reaction_chance * 1.5)
                cut_percentage = min(0.95, cut_percentage * 1.3)
            
            # War intensity boosts reaction chance
            reaction_chance += (self.price_war_intensity * 0.08)
            reaction_chance = min(0.98, reaction_chance)
            
            if random.random() < reaction_chance:
                # Calculate the cut
                potential_cut = price_difference * cut_percentage
                
                # In PREDATORY mode, they sometimes cut BELOW our price!
                if self.competitor_strategy == "PREDATORY" and random.random() < 0.4:
                    potential_cut += random.uniform(0.01, 0.08)  # Undercut us!
                
                new_price = competitor_price - potential_cut
                
                # Competitor minimum price (they'll go as low as cost + 25% in war)
                min_price = product_cost * (1.25 if self.price_war_intensity >= 7 else 1.4)
                new_price = max(min_price, new_price)
                
                old_price = self.competitor_prices[product_name]
                self.competitor_prices[product_name] = round(new_price, 2)
                
                if abs(new_price - old_price) > 0.01:
                    # Determine reaction type
                    if potential_cut > 0.15:
                        reaction_type = "💀 NUCLEAR STRIKE"
                    elif potential_cut > 0.10:
                        reaction_type = "⚔️ AGGRESSIVE ASSAULT"
                    elif potential_cut > 0.05:
                        reaction_type = "🔥 FIERCE COUNTER"
                    else:
                        reaction_type = "⚡ QUICK STRIKE"
                        
                    reactions.append(f"{product_name}: ${old_price:.2f} → ${new_price:.2f} ({reaction_type})")
        
        return reactions
    
    def _execute_proactive_strategy(self, current_prices: Dict[str, float]) -> List[str]:
        """Competitor initiates price cuts to start fights!"""
        reactions = []
        
        # Don't attack every day - make it strategic
        attack_chance = {
            "AGGRESSIVE": 0.35,
            "PREDATORY": 0.45,
            "PSYCHOLOGICAL": 0.25,
            "DEFENSIVE": 0.05,
            "BALANCED": 0.15
        }.get(self.competitor_strategy, 0.15)
        
        # More likely to attack if it's been a while
        attack_chance += (self.days_since_last_attack * 0.05)
        
        # Revenge mode makes them attack more often
        if self.competitor_revenge_mode:
            attack_chance *= 1.8
            
        if random.random() < attack_chance:
            # Pick 1-3 products to attack
            num_attacks = random.randint(1, 3)
            products_to_attack = random.sample(list(PRODUCTS.keys()), num_attacks)
            
            for product_name in products_to_attack:
                old_price = self.competitor_prices[product_name]
                product_cost = PRODUCTS[product_name].cost
                our_price = current_prices[product_name]
                
                # Different attack strategies
                if self.competitor_strategy == "PREDATORY":
                    # Cut to just above cost to crush margins
                    new_price = max(product_cost * 1.25, old_price * 0.85)
                elif self.competitor_strategy == "AGGRESSIVE":
                    # Standard aggressive cut
                    new_price = max(product_cost * 1.3, old_price * 0.9)
                else:
                    # Moderate cut to test our response
                    new_price = max(product_cost * 1.4, old_price * 0.95)
                
                # Sometimes aim to just undercut us
                if our_price < old_price and random.random() < 0.6:
                    new_price = max(new_price, our_price - random.uniform(0.01, 0.05))
                
                self.competitor_prices[product_name] = round(new_price, 2)
                
                if abs(new_price - old_price) > 0.01:
                    attack_type = "🚀 SURPRISE ATTACK" if self.competitor_strategy == "PREDATORY" else "⚡ PROACTIVE STRIKE"
                    reactions.append(f"{product_name}: ${old_price:.2f} → ${new_price:.2f} ({attack_type})")
                    
            if reactions:
                self.days_since_last_attack = 0
        
        return reactions
    
    def _execute_psychological_warfare(self) -> List[str]:
        """Dirty tactics to mess with Scrooge's head"""
        reactions = []
        
        if self.competitor_strategy != "PSYCHOLOGICAL":
            return reactions
            
        # Psychological tactics
        if random.random() < 0.3:  # 30% chance of psychological move
            tactic = random.choice([
                "FAKE_RETREAT",  # Raise prices to make us think we won, then attack
                "LOSS_LEADER",   # Cut one product to loss to steal customers
                "RANDOM_CHAOS"   # Make unpredictable moves to confuse
            ])
            
            if tactic == "FAKE_RETREAT":
                # Raise prices on 1-2 products to fake weakness
                products = random.sample(list(PRODUCTS.keys()), random.randint(1, 2))
                for product_name in products:
                    old_price = self.competitor_prices[product_name]
                    new_price = min(old_price * 1.1, PRODUCTS[product_name].cost * 2.0)
                    self.competitor_prices[product_name] = round(new_price, 2)
                    reactions.append(f"{product_name}: ${old_price:.2f} → ${new_price:.2f} (🎭 FAKE RETREAT)")
                    
            elif tactic == "LOSS_LEADER":
                # Cut one product to barely above cost
                product_name = random.choice(list(PRODUCTS.keys()))
                old_price = self.competitor_prices[product_name]
                cost = PRODUCTS[product_name].cost
                new_price = cost * 1.15  # Very low margin
                self.competitor_prices[product_name] = round(new_price, 2)
                reactions.append(f"{product_name}: ${old_price:.2f} → ${new_price:.2f} (🎯 LOSS LEADER)")
                
            elif tactic == "RANDOM_CHAOS":
                # Make seemingly random moves to confuse
                for product_name in PRODUCTS.keys():
                    if random.random() < 0.4:  # 40% chance per product
                        old_price = self.competitor_prices[product_name]
                        change = random.uniform(-0.08, 0.08)
                        new_price = max(PRODUCTS[product_name].cost * 1.2, old_price + change)
                        self.competitor_prices[product_name] = round(new_price, 2)
                        if abs(new_price - old_price) > 0.01:
                            reactions.append(f"{product_name}: ${old_price:.2f} → ${new_price:.2f} (🌀 CHAOS THEORY)")
        
        return reactions
    
    def _update_war_dynamics(self, reactions: List[str]):
        """Update war intensity and competitor state"""
        if reactions:
            # War escalates with each move
            escalation = len(reactions) * 0.5
            
            # Different strategies escalate differently
            if self.competitor_strategy == "PREDATORY":
                escalation *= 1.5
            elif self.competitor_strategy == "PSYCHOLOGICAL":
                escalation *= 0.8
                
            self.price_war_intensity = min(10, self.price_war_intensity + escalation)
        else:
            # War cools down slowly if no moves
            self.price_war_intensity = max(0, self.price_war_intensity - 0.3)
            
        # Exit revenge mode occasionally
        if self.competitor_revenge_mode and random.random() < 0.1:
            self.competitor_revenge_mode = False
            self.our_total_undercuts *= 0.7  # Reduce anger 
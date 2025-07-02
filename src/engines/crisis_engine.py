import random
from typing import Dict, List, Optional
from src.core.models import (
    CrisisEvent, CrisisType, EmergencyAction, StoreState, MarketEvent, 
    EconomicCondition, WeatherEvent, PRODUCTS, SUPPLIERS, InventoryItem, InventoryBatch
)


class CrisisEngine:
    """🚨 Phase 2C: Crisis Management & Supply Chain Disruption Engine
    
    FEATURES:
    - Supply chain crisis generation based on market conditions
    - Supplier bankruptcy and reliability failures
    - Raw material shortages and cost spikes
    - Emergency response system for agent decision-making
    - Crisis escalation and recovery cycles
    - Competitive supply chain intelligence
    """
    
    def __init__(self):
        self.crisis_probability_base = 0.05  # 5% base chance per day
        self.crisis_escalation_chance = 0.3  # 30% chance crisis escalates
        self.recovery_bonus_days = 0  # Days of reduced crisis after resolution
        
        # Crisis type probabilities based on market conditions
        self.crisis_weights = {
            CrisisType.SUPPLIER_BANKRUPTCY: 0.15,
            CrisisType.SUPPLY_SHORTAGE: 0.20,
            CrisisType.DELIVERY_DISRUPTION: 0.25,
            CrisisType.REGULATORY_CRISIS: 0.10,
            CrisisType.ECONOMIC_SHOCK: 0.10,
            CrisisType.RAW_MATERIAL_SPIKE: 0.15,
            CrisisType.COMPETITIVE_DISRUPTION: 0.05
        }
    
    def generate_crisis_events(self, day: int, store_state: StoreState, 
                              market_event: MarketEvent) -> List[CrisisEvent]:
        """🚨 Generate new crisis events based on market conditions"""
        new_crises = []
        
        # Calculate crisis probability based on market conditions
        crisis_probability = self._calculate_crisis_probability(market_event, store_state)
        
        # Check if new crisis occurs
        if random.random() < crisis_probability:
            crisis_type = self._select_crisis_type(market_event)
            crisis_event = self._generate_crisis(crisis_type, day, market_event, store_state)
            new_crises.append(crisis_event)
        
        # Check for crisis escalation
        for crisis in store_state.active_crises:
            if random.random() < self.crisis_escalation_chance:
                escalated_crisis = self._escalate_crisis(crisis, day)
                if escalated_crisis:
                    new_crises.append(escalated_crisis)
        
        return new_crises
    
    def update_active_crises(self, store_state: StoreState) -> Dict:
        """⏰ Update active crises, remove expired ones"""
        crisis_updates = {
            "resolved_crises": [],
            "ongoing_crises": [],
            "crisis_costs": 0.0
        }
        
        active_crises = []
        
        for crisis in store_state.active_crises:
            crisis.remaining_days -= 1
            
            # Apply daily crisis costs
            daily_cost = self._calculate_daily_crisis_cost(crisis, store_state)
            crisis_updates["crisis_costs"] += daily_cost
            
            if crisis.remaining_days <= 0:
                crisis_updates["resolved_crises"].append(crisis)
                # Apply recovery bonus
                self.recovery_bonus_days = max(3, crisis.duration_days // 2)
            else:
                active_crises.append(crisis)
                crisis_updates["ongoing_crises"].append(crisis)
        
        store_state.active_crises = active_crises
        return crisis_updates
    
    def get_crisis_affected_suppliers(self, store_state: StoreState, 
                                    product_name: str) -> List[Dict]:
        """🏭 Get suppliers affected by current crises"""
        affected_suppliers = []
        
        if product_name not in SUPPLIERS:
            return affected_suppliers
        
        for supplier in SUPPLIERS[product_name]:
            supplier_info = {
                "supplier": supplier,
                "crisis_effects": {
                    "cost_multiplier": 1.0,
                    "delivery_delay": 0,
                    "reliability_penalty": 0.0,
                    "available": True
                }
            }
            
            # Check if supplier is affected by any active crisis
            for crisis in store_state.active_crises:
                if (supplier.name in crisis.affected_suppliers or 
                    product_name in crisis.affected_products):
                    
                    # Apply crisis effects
                    supplier_info["crisis_effects"]["cost_multiplier"] *= crisis.cost_multiplier
                    supplier_info["crisis_effects"]["delivery_delay"] += int(
                        supplier.delivery_days * (crisis.delivery_delay_multiplier - 1)
                    )
                    supplier_info["crisis_effects"]["reliability_penalty"] += crisis.reliability_penalty
                    
                    # Check if supplier is completely unavailable
                    if (crisis.crisis_type == CrisisType.SUPPLIER_BANKRUPTCY and 
                        supplier.name in crisis.affected_suppliers):
                        supplier_info["crisis_effects"]["available"] = False
            
            affected_suppliers.append(supplier_info)
        
        return affected_suppliers
    
    def get_emergency_actions(self, store_state: StoreState) -> List[Dict]:
        """🆘 Get available emergency actions based on current crises"""
        emergency_actions = []
        
        for crisis in store_state.active_crises:
            for action_type in crisis.emergency_actions_available:
                action_info = self._get_emergency_action_info(action_type, crisis, store_state)
                if action_info:
                    emergency_actions.append(action_info)
        
        return emergency_actions
    
    def execute_emergency_action(self, action_type: str, parameters: Dict,
                                store_state: StoreState) -> Dict:
        """⚡ Execute emergency action and return results"""
        
        if action_type == EmergencyAction.EMERGENCY_RESTOCK:
            return self._execute_emergency_restock(parameters, store_state)
        elif action_type == EmergencyAction.SWITCH_SUPPLIER:
            return self._execute_supplier_switch(parameters, store_state)
        elif action_type == EmergencyAction.TAKE_LOAN:
            return self._execute_emergency_loan(parameters, store_state)
        elif action_type == EmergencyAction.COMPETITOR_INTELLIGENCE:
            return self._execute_competitor_intelligence(parameters, store_state)
        else:
            return {"success": False, "message": f"Unknown emergency action: {action_type}"}
    
    def _calculate_crisis_probability(self, market_event: MarketEvent, 
                                    store_state: StoreState) -> float:
        """Calculate probability of crisis based on market conditions"""
        base_prob = self.crisis_probability_base
        
        # Economic condition modifiers
        economic_modifiers = {
            EconomicCondition.NORMAL: 1.0,
            EconomicCondition.BOOM: 0.7,      # Lower crisis chance during boom
            EconomicCondition.RECESSION: 2.5, # Much higher crisis chance during recession
            EconomicCondition.RECOVERY: 1.5   # Moderate crisis chance during recovery
        }
        
        # Weather modifiers
        weather_modifiers = {
            WeatherEvent.NORMAL: 1.0,
            WeatherEvent.HEAT_WAVE: 1.8,      # Supply chain stress
            WeatherEvent.COLD_SNAP: 1.5,      # Delivery disruptions
            WeatherEvent.RAINY_DAY: 2.0,      # Transportation issues
            WeatherEvent.PERFECT_WEATHER: 0.8  # Lower crisis chance
        }
        
        # Apply modifiers
        probability = (base_prob * 
                      economic_modifiers.get(market_event.economic_condition, 1.0) *
                      weather_modifiers.get(market_event.weather, 1.0))
        
        # Recovery bonus reduces crisis chance
        if self.recovery_bonus_days > 0:
            probability *= 0.3
            self.recovery_bonus_days -= 1
        
        # Existing crises reduce chance of new ones
        if store_state.active_crises:
            probability *= 0.4
        
        return min(0.4, probability)  # Cap at 40% max chance
    
    def _select_crisis_type(self, market_event: MarketEvent) -> CrisisType:
        """Select crisis type based on market conditions"""
        weights = self.crisis_weights.copy()
        
        # Adjust weights based on market conditions
        if market_event.economic_condition == EconomicCondition.RECESSION:
            weights[CrisisType.SUPPLIER_BANKRUPTCY] *= 3.0
            weights[CrisisType.ECONOMIC_SHOCK] *= 2.0
        
        if market_event.weather in [WeatherEvent.HEAT_WAVE, WeatherEvent.COLD_SNAP, WeatherEvent.RAINY_DAY]:
            weights[CrisisType.DELIVERY_DISRUPTION] *= 2.5
            weights[CrisisType.SUPPLY_SHORTAGE] *= 1.5
        
        # Select weighted random crisis type
        crisis_types = list(weights.keys())
        weight_values = list(weights.values())
        
        return random.choices(crisis_types, weights=weight_values)[0]
    
    def _generate_crisis(self, crisis_type: CrisisType, day: int, 
                        market_event: MarketEvent, store_state: StoreState) -> CrisisEvent:
        """Generate specific crisis event"""
        
        if crisis_type == CrisisType.SUPPLIER_BANKRUPTCY:
            return self._generate_supplier_bankruptcy(day, market_event)
        elif crisis_type == CrisisType.SUPPLY_SHORTAGE:
            return self._generate_supply_shortage(day, market_event)
        elif crisis_type == CrisisType.DELIVERY_DISRUPTION:
            return self._generate_delivery_disruption(day, market_event)
        elif crisis_type == CrisisType.REGULATORY_CRISIS:
            return self._generate_regulatory_crisis(day, market_event)
        elif crisis_type == CrisisType.ECONOMIC_SHOCK:
            return self._generate_economic_shock(day, market_event)
        elif crisis_type == CrisisType.RAW_MATERIAL_SPIKE:
            return self._generate_raw_material_spike(day, market_event)
        elif crisis_type == CrisisType.COMPETITIVE_DISRUPTION:
            return self._generate_competitive_disruption(day, market_event)
        else:
            # Default crisis
            return CrisisEvent(
                crisis_type=CrisisType.SUPPLY_SHORTAGE,
                severity=0.5,
                duration_days=3,
                remaining_days=3,
                description="General supply chain disruption",
                emergency_actions_available=[EmergencyAction.EMERGENCY_RESTOCK]
            )
    
    def _generate_supplier_bankruptcy(self, day: int, market_event: MarketEvent) -> CrisisEvent:
        """💸 Generate supplier bankruptcy crisis"""
        # Select random product and supplier
        product_name = random.choice(list(SUPPLIERS.keys()))
        suppliers = SUPPLIERS[product_name]
        affected_supplier = random.choice(suppliers)
        
        severity = random.uniform(0.7, 1.0)  # High severity
        duration = random.randint(5, 10)    # 5-10 days to find replacement
        
        return CrisisEvent(
            crisis_type=CrisisType.SUPPLIER_BANKRUPTCY,
            affected_products=[product_name],
            affected_suppliers=[affected_supplier.name],
            severity=severity,
            duration_days=duration,
            remaining_days=duration,
            reliability_penalty=1.0,  # Complete failure
            description=f"💸 SUPPLIER BANKRUPTCY: {affected_supplier.name} has gone bankrupt! {product_name} supply disrupted for {duration} days.",
            emergency_actions_available=[
                EmergencyAction.SWITCH_SUPPLIER,
                EmergencyAction.EMERGENCY_RESTOCK,
                EmergencyAction.RAISE_PRICES
            ]
        )
    
    def _generate_supply_shortage(self, day: int, market_event: MarketEvent) -> CrisisEvent:
        """📦 Generate supply shortage crisis"""
        # Select 1-3 random products
        affected_products = random.sample(list(PRODUCTS.keys()), random.randint(1, 3))
        severity = random.uniform(0.4, 0.8)
        duration = random.randint(3, 7)
        
        return CrisisEvent(
            crisis_type=CrisisType.SUPPLY_SHORTAGE,
            affected_products=affected_products,
            severity=severity,
            duration_days=duration,
            remaining_days=duration,
            cost_multiplier=1.2 + severity * 0.5,  # 20-60% cost increase
            reliability_penalty=0.3 + severity * 0.4,  # 30-70% reliability drop
            description=f"📦 SUPPLY SHORTAGE: {', '.join(affected_products)} shortage! Costs up {((1.2 + severity * 0.5 - 1) * 100):.0f}% for {duration} days.",
            emergency_actions_available=[
                EmergencyAction.EMERGENCY_RESTOCK,
                EmergencyAction.RAISE_PRICES,
                EmergencyAction.LIQUIDATE_INVENTORY
            ]
        )
    
    def _generate_delivery_disruption(self, day: int, market_event: MarketEvent) -> CrisisEvent:
        """🚛 Generate delivery disruption crisis"""
        severity = random.uniform(0.3, 0.9)
        duration = random.randint(2, 5)
        
        # Select affected suppliers (usually all)
        all_suppliers = []
        for suppliers in SUPPLIERS.values():
            all_suppliers.extend([s.name for s in suppliers])
        affected_suppliers = random.sample(all_suppliers, len(all_suppliers) // 2)
        
        return CrisisEvent(
            crisis_type=CrisisType.DELIVERY_DISRUPTION,
            affected_suppliers=affected_suppliers,
            severity=severity,
            duration_days=duration,
            remaining_days=duration,
            delivery_delay_multiplier=1.5 + severity,  # 50-190% longer delivery
            reliability_penalty=0.2 + severity * 0.3,  # 20-50% reliability drop
            description=f"🚛 DELIVERY CRISIS: {market_event.weather.value} causing delivery delays! {len(affected_suppliers)} suppliers affected for {duration} days.",
            emergency_actions_available=[
                EmergencyAction.EMERGENCY_RESTOCK,
                EmergencyAction.SWITCH_SUPPLIER
            ]
        )
    
    def _generate_regulatory_crisis(self, day: int, market_event: MarketEvent) -> CrisisEvent:
        """📋 Generate regulatory/compliance crisis"""
        severity = random.uniform(0.5, 0.9)
        duration = random.randint(7, 14)  # Longer duration
        
        daily_cost = 50 + severity * 150  # $50-200 daily compliance cost
        
        return CrisisEvent(
            crisis_type=CrisisType.REGULATORY_CRISIS,
            severity=severity,
            duration_days=duration,
            remaining_days=duration,
            description=f"📋 REGULATORY CRISIS: Health inspection requires immediate compliance! ${daily_cost:.0f}/day cost for {duration} days.",
            emergency_actions_available=[
                EmergencyAction.TAKE_LOAN,
                EmergencyAction.LIQUIDATE_INVENTORY,
                EmergencyAction.RAISE_PRICES
            ]
        )
    
    def _generate_economic_shock(self, day: int, market_event: MarketEvent) -> CrisisEvent:
        """💹 Generate economic shock crisis"""
        severity = random.uniform(0.6, 1.0)
        duration = random.randint(10, 20)  # Long-lasting
        
        return CrisisEvent(
            crisis_type=CrisisType.ECONOMIC_SHOCK,
            severity=severity,
            duration_days=duration,
            remaining_days=duration,
            cost_multiplier=1.1 + severity * 0.4,  # 10-50% cost increase
            description=f"💹 ECONOMIC SHOCK: Sudden market downturn! All costs up {((1.1 + severity * 0.4 - 1) * 100):.0f}% for {duration} days.",
            emergency_actions_available=[
                EmergencyAction.TAKE_LOAN,
                EmergencyAction.RAISE_PRICES,
                EmergencyAction.COMPETITOR_INTELLIGENCE
            ]
        )
    
    def _generate_raw_material_spike(self, day: int, market_event: MarketEvent) -> CrisisEvent:
        """🏭 Generate raw material cost spike"""
        # Select product category
        affected_products = [name for name, product in PRODUCTS.items() 
                           if random.random() < 0.4]  # 40% chance each product affected
        if not affected_products:
            affected_products = [random.choice(list(PRODUCTS.keys()))]
        
        severity = random.uniform(0.5, 0.9)
        duration = random.randint(4, 8)
        
        return CrisisEvent(
            crisis_type=CrisisType.RAW_MATERIAL_SPIKE,
            affected_products=affected_products,
            severity=severity,
            duration_days=duration,
            remaining_days=duration,
            cost_multiplier=1.3 + severity * 0.7,  # 30-100% cost increase
            description=f"🏭 RAW MATERIAL SPIKE: {', '.join(affected_products)} costs up {((1.3 + severity * 0.7 - 1) * 100):.0f}% for {duration} days!",
            emergency_actions_available=[
                EmergencyAction.RAISE_PRICES,
                EmergencyAction.SWITCH_SUPPLIER,
                EmergencyAction.LIQUIDATE_INVENTORY
            ]
        )
    
    def _generate_competitive_disruption(self, day: int, market_event: MarketEvent) -> CrisisEvent:
        """⚔️ Generate competitive supply chain disruption"""
        severity = random.uniform(0.3, 0.7)
        duration = random.randint(3, 6)
        
        return CrisisEvent(
            crisis_type=CrisisType.COMPETITIVE_DISRUPTION,
            severity=severity,
            duration_days=duration,
            remaining_days=duration,
            description=f"⚔️ COMPETITOR SUPPLY CRISIS: Rival store has supply chain problems! Market opportunity for {duration} days.",
            emergency_actions_available=[
                EmergencyAction.COMPETITOR_INTELLIGENCE,
                EmergencyAction.RAISE_PRICES,
                EmergencyAction.EMERGENCY_RESTOCK
            ]
        )
    
    def _escalate_crisis(self, crisis: CrisisEvent, day: int) -> Optional[CrisisEvent]:
        """📈 Escalate existing crisis to create secondary crisis"""
        if crisis.severity > 0.8:  # Only escalate severe crises
            return None
            
        # Create secondary crisis based on original
        if crisis.crisis_type == CrisisType.SUPPLIER_BANKRUPTCY:
            return self._generate_supply_shortage(day, None)
        elif crisis.crisis_type == CrisisType.DELIVERY_DISRUPTION:
            return self._generate_raw_material_spike(day, None)
        
        return None
    
    def _calculate_daily_crisis_cost(self, crisis: CrisisEvent, store_state: StoreState) -> float:
        """💰 Calculate daily cost of crisis"""
        if crisis.crisis_type == CrisisType.REGULATORY_CRISIS:
            return 50 + crisis.severity * 150  # $50-200 daily
        elif crisis.crisis_type == CrisisType.ECONOMIC_SHOCK:
            return crisis.severity * 30  # $0-30 daily
        return 0.0
    
    def _get_emergency_action_info(self, action_type: str, crisis: CrisisEvent, 
                                  store_state: StoreState) -> Optional[Dict]:
        """Get information about emergency action"""
        if action_type == EmergencyAction.EMERGENCY_RESTOCK:
            return {
                "action": action_type,
                "name": "Emergency Restock",
                "description": "Pay 200% premium for immediate delivery (1 day)",
                "cost": "2x normal cost",
                "crisis": crisis.crisis_type
            }
        elif action_type == EmergencyAction.TAKE_LOAN:
            return {
                "action": action_type,
                "name": "Emergency Loan",
                "description": "Take $500 emergency loan (10% interest)",
                "cost": "$50 interest",
                "crisis": crisis.crisis_type
            }
        elif action_type == EmergencyAction.COMPETITOR_INTELLIGENCE:
            return {
                "action": action_type,
                "name": "Competitor Intelligence",
                "description": "Spy on competitor supply chain weaknesses",
                "cost": "$100",
                "crisis": crisis.crisis_type
            }
        
        return None
    
    def _execute_emergency_restock(self, parameters: Dict, store_state: StoreState) -> Dict:
        """⚡ Execute emergency restock action"""
        product_name = parameters.get("product_name")
        quantity = parameters.get("quantity", 10)
        
        if not product_name or product_name not in PRODUCTS:
            return {"success": False, "message": "Invalid product for emergency restock"}
        
        # Emergency restock costs 200% premium
        product = PRODUCTS[product_name]
        emergency_cost = product.cost * quantity * 2.0
        
        if emergency_cost > store_state.cash:
            return {"success": False, "message": f"Insufficient cash for emergency restock (need ${emergency_cost:.2f})"}
        
        # Process emergency delivery
        store_state.cash -= emergency_cost
        
        # Add inventory immediately (emergency delivery)
        if product_name not in store_state.inventory:
            store_state.inventory[product_name] = InventoryItem(product_name=product_name)
        
        # Add emergency batch
        emergency_batch = InventoryBatch(
            quantity=quantity,
            received_day=store_state.day,
            expiration_day=store_state.day + product.shelf_life_days if product.shelf_life_days else None
        )
        store_state.inventory[product_name].batches.append(emergency_batch)
        
        return {
            "success": True,
            "message": f"EMERGENCY RESTOCK: {quantity} {product_name} delivered immediately for ${emergency_cost:.2f}",
            "cost": emergency_cost
        }
    
    def _execute_supplier_switch(self, parameters: Dict, store_state: StoreState) -> Dict:
        """🔄 Execute emergency supplier switch"""
        # This would integrate with supplier engine for emergency supplier changes
        return {"success": True, "message": "Emergency supplier switch executed", "cost": 25}
    
    def _execute_emergency_loan(self, parameters: Dict, store_state: StoreState) -> Dict:
        """💰 Execute emergency loan"""
        loan_amount = 500
        interest = 50
        
        store_state.crisis_response_cash += loan_amount
        store_state.cash += loan_amount
        store_state.accounts_payable += interest
        
        return {
            "success": True,
            "message": f"EMERGENCY LOAN: ${loan_amount} received, ${interest} interest due",
            "cost": interest
        }
    
    def _execute_competitor_intelligence(self, parameters: Dict, store_state: StoreState) -> Dict:
        """🕵️ Execute competitor intelligence gathering"""
        intelligence_cost = 100
        
        if intelligence_cost > store_state.cash:
            return {"success": False, "message": "Insufficient cash for intelligence operation"}
        
        store_state.cash -= intelligence_cost
        
        # Generate competitive intelligence
        intel_report = self._generate_competitor_intel()
        
        return {
            "success": True,
            "message": f"COMPETITOR INTEL: {intel_report}",
            "cost": intelligence_cost,
            "intelligence": intel_report
        }
    
    def _generate_competitor_intel(self) -> str:
        """🕵️ Generate competitor intelligence report"""
        intel_options = [
            "Competitor has supply shortage in Chips - vulnerable to price attack!",
            "Rival store has cash flow problems - opportunity to steal customers!",
            "Competitor's main supplier is unreliable - they'll have stockouts soon!",
            "Intelligence suggests competitor is planning price war - prepare defenses!",
            "Rival store has regulatory compliance issues - they're distracted!"
        ]
        return random.choice(intel_options) 
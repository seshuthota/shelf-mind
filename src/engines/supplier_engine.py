from typing import Dict, List
from src.core.models import StoreState, PRODUCTS, SUPPLIERS, DeliveryOrder, PaymentTerm


class SupplierEngine:
    """🏭 Phase 1D: SOPHISTICATED SUPPLIER WARFARE SYSTEM 🏭"""
    
    def __init__(self):
        pass
    
    def process_orders(self, orders: Dict[str, int], store_state: StoreState, 
                      crisis_engine=None) -> Dict[str, str]:
        """🏭 Phase 2C: ENHANCED SUPPLIER WARFARE SYSTEM WITH CRISIS MANAGEMENT 🏭"""
        results = {}
        
        for product_name, quantity in orders.items():
            if product_name not in PRODUCTS:
                results[product_name] = f"ERROR: Unknown product {product_name}"
                continue
            
            if quantity <= 0:
                results[product_name] = f"ERROR: Invalid quantity {quantity} for {product_name}"
                continue
            
            # 🚨 CRISIS-AWARE SUPPLIER SELECTION: Consider crisis effects
            supplier_result = self._select_optimal_supplier_with_crisis(
                product_name, quantity, store_state, crisis_engine
            )
            
            if supplier_result["success"]:
                supplier = supplier_result["supplier"]
                cost_info = supplier_result["cost_info"]
                crisis_info = supplier_result.get("crisis_info", {})
                
                # Create delivery order with crisis adjustments
                crisis_delivery_delay = crisis_info.get("delivery_delay", 0)
                delivery_order = DeliveryOrder(
                    supplier_name=supplier.name,
                    product_name=product_name,
                    quantity=quantity,
                    cost_per_unit=cost_info["cost_per_unit"],
                    total_cost=cost_info["total_cost"],
                    order_day=store_state.day,
                    delivery_day=store_state.day + supplier.delivery_days + crisis_delivery_delay,
                    payment_terms=supplier.payment_terms,
                    bulk_discount_applied=cost_info["bulk_discount_applied"]
                )
                
                # Process payment based on terms
                if supplier.payment_terms == PaymentTerm.UPFRONT:
                    if cost_info["total_cost"] > store_state.cash:
                        results[product_name] = f"ERROR: Not enough cash for {quantity} {product_name} from {supplier.name} (need ${cost_info['total_cost']:.2f}, have ${store_state.cash:.2f})"
                        continue
                    store_state.cash -= cost_info["total_cost"]
                    payment_info = f"PAID ${cost_info['total_cost']:.2f} upfront"
                else:  # NET_30
                    store_state.accounts_payable += cost_info["total_cost"]
                    payment_info = f"${cost_info['total_cost']:.2f} due in 30 days"
                
                # Add to pending deliveries
                store_state.pending_deliveries.append(delivery_order)
                
                # Build success message with supplier intelligence and crisis info
                discount_msg = f" (BULK DISCOUNT {cost_info['discount_rate']:.1%})" if cost_info["bulk_discount_applied"] else ""
                crisis_msg = ""
                if crisis_info.get("delivery_delay", 0) > 0:
                    crisis_msg = f" ⚠️ CRISIS DELAY: +{crisis_info['delivery_delay']} days"
                if crisis_info.get("cost_multiplier", 1.0) > 1.0:
                    crisis_msg += f" 💰 CRISIS PREMIUM: +{((crisis_info['cost_multiplier'] - 1) * 100):.0f}%"
                
                total_delivery_days = supplier.delivery_days + crisis_info.get("delivery_delay", 0)
                results[product_name] = f"SUCCESS: Ordered {quantity} {product_name} from {supplier.name} - Delivery in {total_delivery_days} days, {payment_info}{discount_msg}{crisis_msg}"
            else:
                results[product_name] = supplier_result["error"]
        
        return results
    
    def _select_optimal_supplier(self, product_name: str, quantity: int) -> Dict:
        """🎯 SUPPLIER SELECTION WARFARE: Choose optimal supplier based on strategic factors"""
        if product_name not in SUPPLIERS:
            return {"success": False, "error": f"No suppliers available for {product_name}"}
        
        available_suppliers = SUPPLIERS[product_name]
        base_cost = PRODUCTS[product_name].cost
        
        supplier_options = []
        
        for supplier in available_suppliers:
            # Calculate actual cost with supplier pricing
            cost_per_unit = base_cost * supplier.price_multiplier
            
            # Check for bulk discount
            bulk_discount_applied = quantity >= supplier.bulk_discount_threshold
            if bulk_discount_applied:
                cost_per_unit *= (1 - supplier.bulk_discount_rate)
            
            total_cost = cost_per_unit * quantity
            
            # Strategic scoring system
            # Factors: cost, speed, reliability, cash flow impact
            cost_score = 100 - (supplier.price_multiplier * 50)  # Lower cost = higher score
            speed_score = 100 - (supplier.delivery_days * 20)    # Faster = higher score  
            reliability_score = supplier.reliability * 100       # Higher reliability = higher score
            cash_flow_score = 50 if supplier.payment_terms == PaymentTerm.NET_30 else 0  # NET_30 = cash flow advantage
            
            # Bulk discount bonus
            bulk_bonus = 25 if bulk_discount_applied else 0
            
            # Overall strategic value
            total_score = cost_score + speed_score + reliability_score + cash_flow_score + bulk_bonus
            
            supplier_options.append({
                "supplier": supplier,
                "cost_per_unit": cost_per_unit,
                "total_cost": total_cost,
                "bulk_discount_applied": bulk_discount_applied,
                "discount_rate": supplier.bulk_discount_rate if bulk_discount_applied else 0,
                "strategic_score": total_score,
                "delivery_days": supplier.delivery_days,
                "reliability": supplier.reliability
            })
        
        # Select supplier with highest strategic score
        best_supplier = max(supplier_options, key=lambda x: x["strategic_score"])
        
        return {
            "success": True,
            "supplier": best_supplier["supplier"],
            "cost_info": {
                "cost_per_unit": best_supplier["cost_per_unit"],
                "total_cost": best_supplier["total_cost"],
                "bulk_discount_applied": best_supplier["bulk_discount_applied"],
                "discount_rate": best_supplier["discount_rate"]
            }
        }
    
    def _select_optimal_supplier_with_crisis(self, product_name: str, quantity: int,
                                           store_state: StoreState, crisis_engine) -> Dict:
        """🚨 Phase 2C: Crisis-aware supplier selection with dynamic crisis effects"""
        if product_name not in SUPPLIERS:
            return {"success": False, "error": f"No suppliers available for {product_name}"}
        
        # Get crisis-affected suppliers if crisis engine available
        if crisis_engine:
            affected_suppliers = crisis_engine.get_crisis_affected_suppliers(store_state, product_name)
        else:
            # Fallback to normal supplier selection
            return self._select_optimal_supplier(product_name, quantity)
        
        base_cost = PRODUCTS[product_name].cost
        supplier_options = []
        
        for supplier_info in affected_suppliers:
            supplier = supplier_info["supplier"]
            crisis_effects = supplier_info["crisis_effects"]
            
            # Skip unavailable suppliers (bankrupted)
            if not crisis_effects["available"]:
                continue
            
            # Calculate cost with crisis effects
            cost_per_unit = base_cost * supplier.price_multiplier * crisis_effects["cost_multiplier"]
            
            # Check for bulk discount
            bulk_discount_applied = quantity >= supplier.bulk_discount_threshold
            if bulk_discount_applied:
                cost_per_unit *= (1 - supplier.bulk_discount_rate)
            
            total_cost = cost_per_unit * quantity
            
            # Adjust reliability for crisis effects
            effective_reliability = max(0.1, supplier.reliability - crisis_effects["reliability_penalty"])
            
            # Strategic scoring with crisis considerations
            cost_score = 100 - (supplier.price_multiplier * crisis_effects["cost_multiplier"] * 50)
            speed_score = 100 - ((supplier.delivery_days + crisis_effects["delivery_delay"]) * 20)
            reliability_score = effective_reliability * 100
            cash_flow_score = 50 if supplier.payment_terms == PaymentTerm.NET_30 else 0
            
            # Crisis penalty (reduce score for affected suppliers)
            crisis_penalty = 0
            if crisis_effects["cost_multiplier"] > 1.0 or crisis_effects["delivery_delay"] > 0:
                crisis_penalty = 30
            
            # Bulk discount bonus
            bulk_bonus = 25 if bulk_discount_applied else 0
            
            # Overall strategic value
            total_score = cost_score + speed_score + reliability_score + cash_flow_score + bulk_bonus - crisis_penalty
            
            supplier_options.append({
                "supplier": supplier,
                "cost_per_unit": cost_per_unit,
                "total_cost": total_cost,
                "bulk_discount_applied": bulk_discount_applied,
                "discount_rate": supplier.bulk_discount_rate if bulk_discount_applied else 0,
                "strategic_score": total_score,
                "delivery_days": supplier.delivery_days,
                "reliability": effective_reliability,
                "crisis_effects": crisis_effects
            })
        
        if not supplier_options:
            return {"success": False, "error": f"All suppliers for {product_name} are unavailable due to crisis"}
        
        # Select supplier with highest strategic score
        best_supplier = max(supplier_options, key=lambda x: x["strategic_score"])
        
        return {
            "success": True,
            "supplier": best_supplier["supplier"],
            "cost_info": {
                "cost_per_unit": best_supplier["cost_per_unit"],
                "total_cost": best_supplier["total_cost"],
                "bulk_discount_applied": best_supplier["bulk_discount_applied"],
                "discount_rate": best_supplier["discount_rate"]
            },
            "crisis_info": {
                "cost_multiplier": best_supplier["crisis_effects"]["cost_multiplier"],
                "delivery_delay": best_supplier["crisis_effects"]["delivery_delay"],
                "reliability_penalty": best_supplier["crisis_effects"]["reliability_penalty"]
            }
        }
    
    def process_deliveries(self, store_state: StoreState, crisis_engine=None) -> Dict:
        """🚚 Phase 2C: ENHANCED DELIVERY PROCESSING WITH CRISIS EFFECTS"""
        successful_deliveries = []
        failed_deliveries = []
        completed_deliveries = []
        
        for delivery in store_state.pending_deliveries:
            if delivery.delivery_day <= store_state.day:
                # Check if delivery succeeds (supplier reliability with crisis effects)
                supplier = next(s for s in SUPPLIERS[delivery.product_name] if s.name == delivery.supplier_name)
                
                # Calculate effective reliability considering crisis effects
                effective_reliability = supplier.reliability
                if crisis_engine:
                    affected_suppliers = crisis_engine.get_crisis_affected_suppliers(store_state, delivery.product_name)
                    for supplier_info in affected_suppliers:
                        if supplier_info["supplier"].name == delivery.supplier_name:
                            effective_reliability = max(0.1, supplier.reliability - 
                                                      supplier_info["crisis_effects"]["reliability_penalty"])
                            break
                
                if __import__('random').random() <= effective_reliability:
                    # Successful delivery - store_engine will create the batch
                    successful_deliveries.append({
                        "product_name": delivery.product_name,
                        "quantity": delivery.quantity,
                        "supplier": delivery.supplier_name,
                        "cost": delivery.total_cost,
                        "message": f"✅ DELIVERED: {delivery.quantity} {delivery.product_name} from {delivery.supplier_name}"
                    })
                else:
                    # Delivery failed - supplier reliability issue
                    if delivery.payment_terms == PaymentTerm.UPFRONT:
                        # Refund for failed upfront payment
                        store_state.cash += delivery.total_cost
                    else:
                        # Remove from accounts payable
                        store_state.accounts_payable -= delivery.total_cost
                    
                    failed_deliveries.append({
                        "product_name": delivery.product_name,
                        "quantity": delivery.quantity,
                        "supplier": delivery.supplier_name,
                        "cost": delivery.total_cost,
                        "message": f"❌ DELIVERY FAILED: {delivery.supplier_name} failed to deliver {delivery.quantity} {delivery.product_name} (reliability issue)"
                    })
                
                completed_deliveries.append(delivery)
        
        # Remove completed deliveries
        store_state.pending_deliveries = [d for d in store_state.pending_deliveries if d not in completed_deliveries]
        
        return {
            "successful_deliveries": successful_deliveries,
            "failed_deliveries": failed_deliveries,
            "total_delivered": len(successful_deliveries),
            "total_failed": len(failed_deliveries)
        }
    
    def process_payment_obligations(self, store_state: StoreState) -> Dict:
        """💰 PAYMENT PROCESSING: Handle NET-30 payment obligations"""
        # For now, we'll assume all NET-30 payments are due immediately at month end
        # In a more complex system, we'd track individual payment due dates
        
        if store_state.accounts_payable > 0:
            if store_state.accounts_payable <= store_state.cash:
                # Pay all outstanding obligations
                paid_amount = store_state.accounts_payable
                store_state.cash -= paid_amount
                store_state.accounts_payable = 0
                return {
                    "success": True,
                    "message": f"💰 PAID NET-30 OBLIGATIONS: ${paid_amount:.2f}",
                    "remaining_payable": 0
                }
            else:
                # Insufficient cash - partial payment or credit issues
                return {
                    "success": False,
                    "message": f"⚠️  CASH FLOW CRISIS: Need ${store_state.accounts_payable:.2f}, only have ${store_state.cash:.2f}",
                    "remaining_payable": store_state.accounts_payable
                }
        
        return {"success": True, "message": "No outstanding obligations", "remaining_payable": 0}
    
    def get_supplier_info(self) -> Dict:
        """🏭 Phase 1D: Build supplier intelligence briefing"""
        supplier_info = {}
        for product_name, suppliers_list in SUPPLIERS.items():
            supplier_info[product_name] = []
            for supplier in suppliers_list:
                supplier_info[product_name].append({
                    "name": supplier.name,
                    "price_multiplier": supplier.price_multiplier,
                    "delivery_days": supplier.delivery_days,
                    "reliability": supplier.reliability,
                    "bulk_threshold": supplier.bulk_discount_threshold,
                    "bulk_discount": f"{supplier.bulk_discount_rate:.1%}",
                    "payment_terms": supplier.payment_terms.value
                })
        return supplier_info
    
    def get_pending_deliveries_summary(self, store_state: StoreState) -> List[Dict]:
        """Get summary of pending deliveries"""
        pending_summary = []
        for delivery in store_state.pending_deliveries:
            days_remaining = delivery.delivery_day - store_state.day
            pending_summary.append({
                "product": delivery.product_name,
                "quantity": delivery.quantity,
                "supplier": delivery.supplier_name,
                "days_remaining": days_remaining,
                "total_cost": delivery.total_cost
            })
        return pending_summary 
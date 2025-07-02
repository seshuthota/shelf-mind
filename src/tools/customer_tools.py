"""
💖 Elle's Customer Psychology Tools - Separated from agent logic
"""
from typing import Dict

class CustomerTools:
    """💖 Elle's 5 Customer Psychology Tools"""
    
    def customer_satisfaction_analyzer(self, store_status: Dict, context: Dict) -> Dict:
        """💝 TOOL 1: Advanced customer satisfaction analysis and sentiment monitoring"""
        inventory = store_status.get('inventory', {})
        yesterday_summary = context.get('yesterday_summary', {})
        current_prices = store_status.get('current_prices', {})
        
        satisfaction_analysis = {
            'satisfaction_metrics': {},
            'customer_sentiment_score': 0,
            'satisfaction_drivers': [],
            'dissatisfaction_risks': [],
            'improvement_opportunities': []
        }
        
        # Analyze satisfaction by segment
        total_customers = yesterday_summary.get('total_customers', 0)
        price_sensitive_customers = yesterday_summary.get('price_sensitive_customers', 0)
        brand_loyal_customers = yesterday_summary.get('brand_loyal_customers', 0)
        
        satisfaction_analysis['satisfaction_metrics'] = {
            'total_customers': total_customers,
            'price_sensitive_ratio': round(price_sensitive_customers / total_customers, 2) if total_customers > 0 else 0,
            'brand_loyal_ratio': round(brand_loyal_customers / total_customers, 2) if total_customers > 0 else 0,
            'customer_diversity_score': min(price_sensitive_customers, brand_loyal_customers) / max(price_sensitive_customers, brand_loyal_customers, 1)
        }
        
        # Customer sentiment analysis - handle both dict and int inventory values
        stockouts = 0
        low_stock = 0
        for qty in inventory.values():
            # Convert dict/object to actual quantity
            if isinstance(qty, dict):
                actual_qty = qty.get('total_quantity', 0)
            elif hasattr(qty, 'total_quantity'):
                actual_qty = qty.total_quantity
            else:
                actual_qty = qty
                
            if actual_qty == 0:
                stockouts += 1
            elif 0 < actual_qty <= 2:
                low_stock += 1
                
        total_products = len(inventory)
        
        # Base sentiment calculation
        availability_score = ((total_products - stockouts) / total_products) * 100 if total_products > 0 else 100
        variety_score = 100 - (low_stock * 5)  # Each low stock reduces by 5%
        
        # Customer volume indicator
        if total_customers >= 15:
            volume_satisfaction = 85  # High traffic = satisfaction
            satisfaction_analysis['satisfaction_drivers'].append("High customer traffic indicates strong satisfaction")
        elif total_customers >= 10:
            volume_satisfaction = 70
        else:
            volume_satisfaction = 50
            satisfaction_analysis['dissatisfaction_risks'].append("Low customer traffic may indicate dissatisfaction")
        
        # Overall sentiment score
        satisfaction_analysis['customer_sentiment_score'] = round((availability_score + variety_score + volume_satisfaction) / 3, 1)
        
        # Identify satisfaction drivers
        if stockouts == 0:
            satisfaction_analysis['satisfaction_drivers'].append("Perfect product availability maintains customer trust")
        if satisfaction_analysis['satisfaction_metrics']['customer_diversity_score'] > 0.7:
            satisfaction_analysis['satisfaction_drivers'].append("Balanced customer segments indicate broad appeal")
        
        # Identify dissatisfaction risks
        if stockouts > 0:
            satisfaction_analysis['dissatisfaction_risks'].append(f"{stockouts} stockouts creating customer disappointment")
        if satisfaction_analysis['satisfaction_metrics']['price_sensitive_ratio'] > 0.8:
            satisfaction_analysis['dissatisfaction_risks'].append("Over-reliance on price-sensitive customers")
        
        # Improvement opportunities
        if satisfaction_analysis['customer_sentiment_score'] < 70:
            satisfaction_analysis['improvement_opportunities'].append("Implement immediate satisfaction recovery program")
        if stockouts > 0:
            satisfaction_analysis['improvement_opportunities'].append("Emergency stock replenishment to prevent customer loss")
        if total_customers < 10:
            satisfaction_analysis['improvement_opportunities'].append("Customer acquisition campaign needed")
            
        return satisfaction_analysis
    
    def loyalty_program_optimizer(self, store_status: Dict, context: Dict) -> Dict:
        """👑 TOOL 2: Customer loyalty program optimization and retention strategies"""
        yesterday_summary = context.get('yesterday_summary', {})
        current_prices = store_status.get('current_prices', {})
        
        loyalty_strategy = {
            'segment_strategies': {},
            'retention_programs': {},
            'engagement_tactics': {},
            'loyalty_metrics': {},
            'program_recommendations': []
        }
        
        # Analyze customer segments for loyalty programs
        price_sensitive_revenue = yesterday_summary.get('price_sensitive_revenue', 0)
        brand_loyal_revenue = yesterday_summary.get('brand_loyal_revenue', 0)
        total_revenue = price_sensitive_revenue + brand_loyal_revenue
        
        if total_revenue > 0:
            # Price-sensitive customer strategy
            loyalty_strategy['segment_strategies']['price_sensitive'] = {
                'revenue_share': round((price_sensitive_revenue / total_revenue) * 100, 1),
                'retention_approach': 'value_rewards',
                'key_tactics': ['points_for_savings', 'bulk_discounts', 'price_alerts'],
                'engagement_frequency': 'high_touch'
            }
            
            # Brand-loyal customer strategy  
            loyalty_strategy['segment_strategies']['brand_loyal'] = {
                'revenue_share': round((brand_loyal_revenue / total_revenue) * 100, 1),
                'retention_approach': 'premium_experience',
                'key_tactics': ['exclusive_access', 'premium_service', 'early_notifications'],
                'engagement_frequency': 'quality_touch'
            }
        
        # Design retention programs
        loyalty_strategy['retention_programs'] = {
            'points_system': {
                'earn_rate': '1 point per $1 spent',
                'redemption_value': '$0.05 per point',
                'bonus_multipliers': {'weekends': '2x', 'new_products': '3x'},
                'tier_benefits': {'bronze': '5%', 'silver': '10%', 'gold': '15%'}
            },
            'vip_membership': {
                'qualification': '$50+ monthly spend',
                'benefits': ['priority_service', 'exclusive_offers', 'early_access'],
                'engagement_perks': ['personal_shopper', 'custom_recommendations']
            },
            'referral_program': {
                'reward_structure': '$5 for referrer, $5 for new customer',
                'bonus_periods': 'double rewards monthly',
                'social_integration': 'Instagram contest entries'
            }
        }
        
        # Engagement tactics
        loyalty_strategy['engagement_tactics'] = {
            'personalization': {
                'product_recommendations': 'Based on purchase history',
                'customized_offers': 'Segment-specific promotions',
                'birthday_rewards': 'Special celebration discounts'
            },
            'communication': {
                'welcome_series': '3-email onboarding sequence',
                'regular_updates': 'Weekly newsletter with tips',
                'satisfaction_surveys': 'Monthly feedback collection'
            },
            'experiential': {
                'exclusive_events': 'VIP customer tastings',
                'early_access': 'New product previews',
                'behind_scenes': 'Business insights sharing'
            }
        }
        
        # Calculate loyalty metrics
        repeat_customer_rate = 0.6  # Assumed based on segments
        average_purchase_frequency = 2.1  # Assumed
        
        loyalty_strategy['loyalty_metrics'] = {
            'repeat_customer_rate': round(repeat_customer_rate * 100, 1),
            'purchase_frequency': average_purchase_frequency,
            'customer_lifetime_value': round(total_revenue * repeat_customer_rate * 12, 2),
            'loyalty_score': round((repeat_customer_rate + (average_purchase_frequency / 5)) * 50, 1)
        }
        
        # Program recommendations
        loyalty_strategy['program_recommendations'] = [
            "Launch tiered loyalty program with instant gratification",
            "Implement personalized product recommendations",
            "Create VIP experience for high-value customers", 
            "Develop social media engagement campaigns",
            "Establish customer feedback loop for continuous improvement"
        ]
        
        return loyalty_strategy
    
    def brand_sentiment_monitor(self, store_status: Dict, context: Dict) -> Dict:
        """✨ TOOL 3: Brand sentiment monitoring and reputation management"""
        inventory = store_status.get('inventory', {})
        yesterday_summary = context.get('yesterday_summary', {})
        current_prices = store_status.get('current_prices', {})
        competitor_prices = store_status.get('competitor_prices', {})
        
        sentiment_monitoring = {
            'brand_perception': {},
            'competitive_sentiment': {},
            'reputation_indicators': {},
            'sentiment_trends': {},
            'reputation_action_plan': []
        }
        
        # Brand perception analysis
        total_customers = yesterday_summary.get('total_customers', 0)
        total_revenue = yesterday_summary.get('total_revenue', 0)
        average_transaction = total_revenue / total_customers if total_customers > 0 else 0
        
        sentiment_monitoring['brand_perception'] = {
            'customer_volume_trend': 'growing' if total_customers >= 12 else 'stable' if total_customers >= 8 else 'declining',
            'transaction_value_trend': 'premium' if average_transaction >= 8 else 'value' if average_transaction >= 5 else 'budget',
            'brand_positioning': 'quality_leader' if average_transaction >= 8 else 'value_provider',
            'customer_loyalty_indicator': 'high' if total_customers >= 15 else 'medium' if total_customers >= 10 else 'low'
        }
        
        # Competitive sentiment analysis
        competitive_advantages = 0
        competitive_disadvantages = 0
        
        for product, our_price in current_prices.items():
            competitor_price = competitor_prices.get(product, our_price)
            
            if our_price < competitor_price:
                competitive_advantages += 1
            elif our_price > competitor_price:
                competitive_disadvantages += 1
        
        sentiment_monitoring['competitive_sentiment'] = {
            'price_competitiveness': 'leading' if competitive_advantages > competitive_disadvantages else 'following',
            'market_position_strength': round((competitive_advantages / len(current_prices)) * 100, 1) if current_prices else 0,
            'competitive_pressure': 'high' if competitive_disadvantages > 3 else 'medium' if competitive_disadvantages > 1 else 'low'
        }
        
        # Reputation indicators - handle both dict and int inventory values
        stockouts = 0
        low_stock = 0
        for qty in inventory.values():
            # Convert dict/object to actual quantity
            if isinstance(qty, dict):
                actual_qty = qty.get('total_quantity', 0)
            elif hasattr(qty, 'total_quantity'):
                actual_qty = qty.total_quantity
            else:
                actual_qty = qty
                
            if actual_qty == 0:
                stockouts += 1
            elif 0 < actual_qty <= 2:
                low_stock += 1
        
        reputation_score = 100
        reputation_score -= stockouts * 15  # Major penalty for stockouts
        reputation_score -= low_stock * 5   # Minor penalty for low stock
        reputation_score += min(total_customers, 20)  # Bonus for high traffic
        
        sentiment_monitoring['reputation_indicators'] = {
            'overall_reputation_score': max(0, reputation_score),
            'service_reliability': 'excellent' if stockouts == 0 else 'good' if stockouts <= 1 else 'poor',
            'customer_experience_quality': 'premium' if reputation_score >= 100 else 'standard' if reputation_score >= 80 else 'needs_improvement',
            'word_of_mouth_potential': 'positive' if reputation_score >= 90 else 'neutral' if reputation_score >= 70 else 'negative'
        }
        
        # Sentiment trends
        sentiment_monitoring['sentiment_trends'] = {
            'trajectory': 'improving' if stockouts == 0 and total_customers >= 12 else 'declining' if stockouts > 1 else 'stable',
            'momentum_indicators': [],
            'risk_factors': [],
            'opportunity_signals': []
        }
        
        # Add momentum indicators
        if total_customers >= 15:
            sentiment_monitoring['sentiment_trends']['momentum_indicators'].append("High customer traffic building positive buzz")
        if competitive_advantages > competitive_disadvantages:
            sentiment_monitoring['sentiment_trends']['momentum_indicators'].append("Price leadership creating value perception")
        
        # Add risk factors
        if stockouts > 0:
            sentiment_monitoring['sentiment_trends']['risk_factors'].append("Stockouts damaging reliability reputation")
        if competitive_disadvantages > 2:
            sentiment_monitoring['sentiment_trends']['risk_factors'].append("Price disadvantage hurting value perception")
        
        # Add opportunity signals
        if sentiment_monitoring['brand_perception']['customer_loyalty_indicator'] == 'high':
            sentiment_monitoring['sentiment_trends']['opportunity_signals'].append("Strong loyalty base for premium positioning")
        
        # Reputation action plan
        reputation_score = sentiment_monitoring['reputation_indicators']['overall_reputation_score']
        if reputation_score < 80:
            sentiment_monitoring['reputation_action_plan'].append("Implement reputation recovery strategy")
        if stockouts > 0:
            sentiment_monitoring['reputation_action_plan'].append("Address inventory issues to protect reliability reputation")
        if sentiment_monitoring['competitive_sentiment']['competitive_pressure'] == 'high':
            sentiment_monitoring['reputation_action_plan'].append("Develop competitive response to maintain market position")
        
        return sentiment_monitoring
    
    def service_quality_metrics(self, store_status: Dict, context: Dict) -> Dict:
        """⭐ TOOL 4: Comprehensive service quality measurement and optimization"""
        inventory = store_status.get('inventory', {})
        yesterday_summary = context.get('yesterday_summary', {})
        
        service_metrics = {
            'availability_metrics': {},
            'convenience_scores': {},
            'customer_experience_kpis': {},
            'service_quality_index': 0,
            'improvement_priorities': []
        }
        
        # Availability metrics - handle both dict and int inventory values
        total_products = len(inventory)
        stocked_products = 0
        well_stocked_products = 0
        
        for qty in inventory.values():
            # Convert dict/object to actual quantity
            if isinstance(qty, dict):
                actual_qty = qty.get('total_quantity', 0)
            elif hasattr(qty, 'total_quantity'):
                actual_qty = qty.total_quantity
            else:
                actual_qty = qty
                
            if actual_qty > 0:
                stocked_products += 1
            if actual_qty >= 5:
                well_stocked_products += 1
                
        stockouts = total_products - stocked_products
        
        service_metrics['availability_metrics'] = {
            'product_availability_rate': round((stocked_products / total_products) * 100, 1) if total_products > 0 else 100,
            'well_stocked_rate': round((well_stocked_products / total_products) * 100, 1) if total_products > 0 else 100,
            'stockout_rate': round((stockouts / total_products) * 100, 1) if total_products > 0 else 0,
            'inventory_health_score': round(((stocked_products * 0.7) + (well_stocked_products * 0.3)) / total_products * 100, 1) if total_products > 0 else 100
        }
        
        # Convenience scores
        variety_score = min(total_products * 10, 100)  # 10 points per product, max 100
        accessibility_score = 90  # Assumed high accessibility
        
        service_metrics['convenience_scores'] = {
            'product_variety': variety_score,
            'shopping_accessibility': accessibility_score,
            'service_reliability': 100 - (stockouts * 20),  # Penalty for stockouts
            'overall_convenience': round((variety_score + accessibility_score + (100 - stockouts * 20)) / 3, 1)
        }
        
        # Customer experience KPIs
        total_customers = yesterday_summary.get('total_customers', 0)
        total_revenue = yesterday_summary.get('total_revenue', 0)
        
        service_metrics['customer_experience_kpis'] = {
            'customer_satisfaction_proxy': round(total_customers * 5, 1),  # Traffic as satisfaction proxy
            'service_efficiency': round(total_revenue / total_customers, 2) if total_customers > 0 else 0,
            'repeat_visit_likelihood': 'high' if total_customers >= 15 else 'medium' if total_customers >= 10 else 'low',
            'service_consistency': 'excellent' if stockouts == 0 else 'good' if stockouts <= 1 else 'inconsistent'
        }
        
        # Calculate Service Quality Index
        availability_weight = 0.4
        convenience_weight = 0.3  
        experience_weight = 0.3
        
        availability_component = service_metrics['availability_metrics']['product_availability_rate'] * availability_weight
        convenience_component = service_metrics['convenience_scores']['overall_convenience'] * convenience_weight
        experience_component = min(total_customers * 4, 100) * experience_weight  # Customer volume as experience proxy
        
        service_metrics['service_quality_index'] = round(availability_component + convenience_component + experience_component, 1)
        
        # Improvement priorities
        if service_metrics['availability_metrics']['stockout_rate'] > 10:
            service_metrics['improvement_priorities'].append("Critical: Resolve inventory availability issues")
        if service_metrics['convenience_scores']['overall_convenience'] < 80:
            service_metrics['improvement_priorities'].append("Enhance shopping convenience and accessibility")
        if total_customers < 10:
            service_metrics['improvement_priorities'].append("Focus on customer acquisition and experience")
        if service_metrics['service_quality_index'] < 85:
            service_metrics['improvement_priorities'].append("Implement comprehensive service quality program")
        
        return service_metrics
    
    def relationship_building_tools(self, store_status: Dict, context: Dict) -> Dict:
        """💕 TOOL 5: Advanced customer relationship building and engagement strategies"""
        yesterday_summary = context.get('yesterday_summary', {})
        current_prices = store_status.get('current_prices', {})
        
        relationship_tools = {
            'relationship_strategies': {},
            'engagement_programs': {},
            'communication_plans': {},
            'relationship_health_score': 0,
            'connection_opportunities': []
        }
        
        # Analyze current relationship state
        total_customers = yesterday_summary.get('total_customers', 0)
        price_sensitive_customers = yesterday_summary.get('price_sensitive_customers', 0)
        brand_loyal_customers = yesterday_summary.get('brand_loyal_customers', 0)
        
        # Relationship strategies by segment
        if price_sensitive_customers > 0:
            relationship_tools['relationship_strategies']['price_conscious'] = {
                'approach': 'value_partnership',
                'key_messages': ['best_prices', 'savings_opportunities', 'value_delivery'],
                'engagement_style': 'informative_and_helpful',
                'relationship_goal': 'trusted_value_provider',
                'success_metrics': ['repeat_visits', 'referrals', 'price_satisfaction']
            }
        
        if brand_loyal_customers > 0:
            relationship_tools['relationship_strategies']['quality_focused'] = {
                'approach': 'premium_partnership',
                'key_messages': ['quality_assurance', 'exclusive_service', 'personalized_attention'],
                'engagement_style': 'consultative_and_premium',
                'relationship_goal': 'preferred_brand_partner',
                'success_metrics': ['loyalty_retention', 'advocacy', 'premium_purchases']
            }
        
        # Engagement programs
        relationship_tools['engagement_programs'] = {
            'welcome_experience': {
                'new_customer_greeting': 'Personalized welcome and store tour',
                'first_purchase_bonus': '10% discount on first order',
                'introduction_package': 'Sample products and loyalty enrollment',
                'follow_up_sequence': '3-touch welcome series over 2 weeks'
            },
            'ongoing_engagement': {
                'regular_check_ins': 'Weekly satisfaction touchpoints',
                'seasonal_celebrations': 'Holiday and birthday recognition',
                'exclusive_previews': 'New product early access',
                'feedback_collection': 'Monthly experience surveys'
            },
            'retention_initiatives': {
                'loyalty_milestones': 'Achievement recognition and rewards',
                'win_back_campaigns': 'Re-engagement for lapsed customers',
                'referral_incentives': 'Social sharing and friend rewards',
                'appreciation_events': 'Customer appreciation celebrations'
            }
        }
        
        # Communication plans
        relationship_tools['communication_plans'] = {
            'frequency_strategy': {
                'high_value_customers': 'weekly_personal_touch',
                'regular_customers': 'bi_weekly_updates',
                'new_customers': 'daily_for_first_week'
            },
            'channel_optimization': {
                'in_store': 'Face-to-face relationship building',
                'digital': 'Email newsletters and social media',
                'community': 'Local events and partnerships',
                'mobile': 'SMS alerts and mobile app engagement'
            },
            'message_personalization': {
                'purchase_history': 'Tailored product recommendations',
                'preference_tracking': 'Customized offers and communications',
                'lifecycle_stage': 'Appropriate messaging for customer journey',
                'value_alignment': 'Messages matching customer values'
            }
        }
        
        # Calculate relationship health score
        customer_diversity = min(price_sensitive_customers, brand_loyal_customers) / max(price_sensitive_customers, brand_loyal_customers, 1)
        customer_volume_score = min(total_customers * 5, 100)
        engagement_potential = (customer_diversity * 50) + (customer_volume_score * 0.5)
        
        relationship_tools['relationship_health_score'] = round(engagement_potential, 1)
        
        # Connection opportunities
        if total_customers >= 15:
            relationship_tools['connection_opportunities'].append("Host customer appreciation event")
        if customer_diversity > 0.7:
            relationship_tools['connection_opportunities'].append("Create community around shared values")
        if price_sensitive_customers > brand_loyal_customers:
            relationship_tools['connection_opportunities'].append("Develop value-focused loyalty program")
        else:
            relationship_tools['connection_opportunities'].append("Create premium experience program")
        
        relationship_tools['connection_opportunities'].extend([
            "Implement personalized shopping experience",
            "Create customer advisory board",
            "Develop social media community",
            "Launch customer success program"
        ])
        
        return relationship_tools

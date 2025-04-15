from math import ceil

# Thruster and Pump classes (reuse your existing code)
class Thruster:
    
    base_consumption = [60, 78, 96, 114, 150]
    base_thrust = [59.95, 72.45, 89.45, 105.95, 139.45]
    
    efficiency_slope = 0.5/(0.8-0.1)
    efficiency_offset_x = 0.1
    efficiency_offset_y = 1.0
    
    consumption_slope = 1.9/(0.8-0.1)
    consumption_offset_x = 0.1
    consumption_offset_y = 0.1
    
    thrust_coefs = [-1.86813187, 2.97340659, -0.1818022]
   
    @classmethod 
    def efficiency(cls, fuel_filled: float) -> float:
        """
        Calculate the efficiency of a thruster given the fuel input.

        Args:
            fuel (float): The amount of fuel.

        Returns:
            float: The efficiency of the thruster.
        """
        # Placeholder for actual efficiency calculation
        # This should be replaced with the actual logic to calculate efficiency
        if fuel_filled <= 0.1:
            return 1.0
        elif fuel_filled >= 0.8:
            return 0.5
        else:
            return cls.efficiency_offset_y - (fuel_filled - cls.efficiency_offset_x) * cls.efficiency_slope
        
    @classmethod
    def efficiency_inv(cls, efficiency: float) -> float:
        """
        Calculate the fuel input given the efficiency.

        Args:
            efficiency (float): The efficiency of the thruster.

        Returns:
            float: The fuel input.
        """
        
        # Placeholder for actual inverse efficiency calculation
        # This should be replaced with the actual logic to calculate inverse efficiency
        if efficiency >= 1.0:
            return 0.1
        elif efficiency <= 0.5:
            return 0.8
        else:
            return (cls.efficiency_offset_y - efficiency) / cls.efficiency_slope + cls.efficiency_offset_x
        

    @classmethod    
    def consumption(cls, fuel_filled: float, quality: int=0) -> float:
        """
        Calculate the consumption of a thruster given the fuel input and quality.

        Args:
            fuel (float): The amount of fuel.

        Returns:
            float: The efficiency of the thruster.
        """
        # Placeholder for actual efficiency calculation
        # This should be replaced with the actual logic to calculate efficiency
        if fuel_filled <= 0.1:
            return 0.1 *  cls.base_consumption[quality]
        elif fuel_filled >= 0.8:
            return 2.0 * cls.base_consumption[quality]
        else:
            return ( cls.consumption_offset_y + (fuel_filled - cls.consumption_offset_x) * cls.consumption_slope ) * cls.base_consumption[quality]
        
    
    @classmethod
    def consumption_inv(cls, consumption: float, quality: int=0) -> float:
        """
        Calculate the fuel input given the consumption.

        Args:
            consumption (float): The consumption of the thruster.

        Returns:
            float: The fuel input.
        """
        
        # Placeholder for actual inverse efficiency calculation
        # This should be replaced with the actual logic to calculate inverse efficiency
        if consumption >= 2.0 * cls.base_consumption[quality]:
            return 0.8
        elif consumption <= 0.1 * cls.base_consumption[quality]:
            return 0.1
        else:
            return (consumption / cls.base_consumption[quality] - cls.consumption_offset_y) / cls.consumption_slope + cls.consumption_offset_x
        
    @classmethod
    def consumption_from_efficiency(cls, efficiency: float, quality: int=0) -> float:
        """
        Calculate the consumption of a thruster given the efficiency.

        Args:
            efficiency (float): The efficiency of the thruster.

        Returns:
            float: The consumption of the thruster.
        """
        
        # Placeholder for actual consumption calculation
        # This should be replaced with the actual logic to calculate consumption from efficiency
        fuel_filled = cls.efficiency_inv(efficiency)
        return cls.consumption(fuel_filled, quality)
    
    @classmethod
    def efficiency_from_consumption(cls, consumption: float, quality: int=0) -> float:
        """
        Calculate the efficiency of a thruster given the consumption.

        Args:
            consumption (float): The consumption of the thruster.

        Returns:
            float: The efficiency of the thruster.
        """
        
        # Placeholder for actual efficiency calculation
        # This should be replaced with the actual logic to calculate efficiency from consumption
        fuel_filled = cls.consumption_inv(consumption, quality)
        return cls.efficiency(fuel_filled)
    

          
    @classmethod  
    def relative_thrust(cls, fuel_filled: float) -> float:
        """
        Calculate the relative thrust of a thruster given the fuel input.

        Args:
            fuel (float): The amount of fuel.

        Returns:
            float: The relative thrust of the thruster.
        """
        
        # Placeholder for actual relative thrust calculation
        # This should be replaced with the actual logic to calculate relative thrust
        if fuel_filled <= 0.1:
            return 0.1
        elif fuel_filled >= 0.75:
            return 1.0
        else:
            return fuel_filled * fuel_filled * cls.thrust_coefs[0] + fuel_filled * cls.thrust_coefs[1] + cls.thrust_coefs[2]
        
        
    @classmethod
    def relative_thrust_from_consumption(cls, consumption: float, quality: int=0) -> float:
        """
        Calculate the relative thrust of a thruster given the consumption.

        Args:
            consumption (float): The consumption of the thruster.

        Returns:
            float: The relative thrust of the thruster.
        """
        
        # Placeholder for actual relative thrust calculation
        # This should be replaced with the actual logic to calculate relative thrust from consumption
        fuel_filled = cls.consumption_inv(consumption, quality)
        return cls.relative_thrust(fuel_filled)
    
class Pump:
    max_flow = [1200, 1560, 1920, 2280, 3000]
    
    @classmethod
    def parameters(cls, target_flow: float, quality:int=0, max_period:int=120) -> (int, int, int, float):
        """
        Calculate the parameters for a pump given the target flow rate.

        Args:
            target_flow (float): The target flow rate.
            quality (int): The quality of the pump.
            clock_period (int): The clock period in milliseconds.

        Returns:
            tuple: A tuple containing the parameters for the pump.
        """
        
        n_pump = ceil(target_flow / cls.max_flow[quality])  
        
        pwm_params = cls.duty_cycle(target_flow / cls.max_flow[quality], max_period=max_period) 
        
        return (n_pump,) + pwm_params
    
    @staticmethod
    def duty_cycle(ratio: float, max_period: int = 120) -> (int, int, float):
        
        best_match = None
        lowest_error = 1.0
        
        for period in range(2, max_period+1):
            ideal_on_ticks = ratio * period
            rounded_on_ticks = int(ideal_on_ticks)
            error = ideal_on_ticks - rounded_on_ticks
            if error == 0.0:
                return (period, rounded_on_ticks, error)
            elif error < lowest_error:
                lowest_error = error
                best_match = (period, rounded_on_ticks, error)
        
        return best_match

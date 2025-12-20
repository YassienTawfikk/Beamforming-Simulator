class ScenarioManager:
    def __init__(self):
        self.scenarios = {
            '5G': {
                'frequency': 30,
                'frequency_bandwidth_index': 2,
                'elements_spacing': 50,
                'curvature': 0,
                'num_elements': 32
            },
            'Ultrasound': {
                'frequency': 100,
                'frequency_bandwidth_index': 2,
                'elements_spacing': 10,
                'curvature': 90,
                'num_elements': 64
            },
            'Tumor Ablation': {
                'frequency': 50,
                'frequency_bandwidth_index': 2,
                'elements_spacing': 15,
                'curvature': 0,
                'num_elements': 128
            }
        }
        self.scenario_names = list(self.scenarios.keys())

    def get_first_scenario(self):
        return '5G'

    def get_next_scenario(self, current_scenario_name):
        if current_scenario_name is None:
            return self.get_first_scenario()
        
        try:
            current_index = self.scenario_names.index(current_scenario_name)
            return self.scenario_names[(current_index + 1) % len(self.scenario_names)]
        except ValueError:
            return self.get_first_scenario()

    def get_scenario_settings(self, scenario_name):
        return self.scenarios.get(scenario_name)

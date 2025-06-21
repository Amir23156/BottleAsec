from ics_sim.Device import PLC, SensorConnector, ActuatorConnector
from Configs import TAG, Controllers, Connection
import logging


class PLC1(PLC):
    def __init__(self):
        sensor_connector = SensorConnector(Connection.CONNECTION)
        actuator_connector = ActuatorConnector(Connection.CONNECTION)
        super().__init__(1, sensor_connector, actuator_connector, TAG.TAG_LIST, Controllers.PLCs)
        
        # BOTTLEASEC : Variables pour gestion commandes d'urgence
        self.emergency_override = False
        self.last_emergency_time = 0
        self.emergency_timeout = 30  # 30 secondes timeout pour commandes d'urgence

    def _logic(self):
        # BOTTLEASEC : Vérifier si des commandes d'urgence sont actives
        self._check_emergency_override()
        
        #  update TAG.TAG_TANK_INPUT_VALVE_STATUS
        if not self._check_manual_input(TAG.TAG_TANK_INPUT_VALVE_MODE, TAG.TAG_TANK_INPUT_VALVE_STATUS):
            # BOTTLEASEC : Respecter les commandes d'urgence
            if not self.emergency_override:
                tank_level = self._get(TAG.TAG_TANK_LEVEL_VALUE)
                if tank_level > self._get(TAG.TAG_TANK_LEVEL_MAX):
                    self._set(TAG.TAG_TANK_INPUT_VALVE_STATUS, 0)
                elif tank_level < self._get(TAG.TAG_TANK_LEVEL_MIN):
                    self._set(TAG.TAG_TANK_INPUT_VALVE_STATUS, 1)

        #  update TAG.TAG_TANK_OUTPUT_VALVE_STATUS
        if not self._check_manual_input(TAG.TAG_TANK_OUTPUT_VALVE_MODE, TAG.TAG_TANK_OUTPUT_VALVE_STATUS):
            # BOTTLEASEC : Respecter les commandes d'urgence
            if not self.emergency_override:
                bottle_level = self._get(TAG.TAG_BOTTLE_LEVEL_VALUE)
                belt_position = self._get(TAG.TAG_BOTTLE_DISTANCE_TO_FILLER_VALUE)
                if bottle_level > self._get(TAG.TAG_BOTTLE_LEVEL_MAX) or belt_position > 1.0:
                    self._set(TAG.TAG_TANK_OUTPUT_VALVE_STATUS, 0)
                else:
                    self._set(TAG.TAG_TANK_OUTPUT_VALVE_STATUS, 1)

    def _check_emergency_override(self):
        """
        BOTTLEASEC : Détection commandes d'urgence HMI3
        Si le niveau dépasse les limites normales ou si des changements
        suspects sont détectés, on suppose une commande d'urgence
        """
        import time
        current_time = time.time()
        
        try:
            # Vérifier si les limites de sécurité ont été modifiées (HMI3 override)
            tank_max = self._get(TAG.TAG_TANK_LEVEL_MAX)
            bottle_max = self._get(TAG.TAG_BOTTLE_LEVEL_MAX)
            
            # Si les limites ont été changées par HMI3 (override sécurité)
            if tank_max > 7.5 or bottle_max > 2.0:
                self.emergency_override = True
                self.last_emergency_time = current_time
                self.report("BOTTLEASEC: Emergency override detected - Safety limits modified", logging.WARNING)
                return
            
            # Vérifier si on est en situation d'urgence (niveau très élevé)
            tank_level = self._get(TAG.TAG_TANK_LEVEL_VALUE)
            if tank_level > 8.0:  # Niveau d'urgence critique
                self.emergency_override = True
                self.last_emergency_time = current_time
                self.report("BOTTLEASEC: Emergency override - Critical tank level", logging.WARNING)
                return
                
        except Exception as e:
            pass
        
        # Désactiver l'override après timeout
        if self.emergency_override and (current_time - self.last_emergency_time) > self.emergency_timeout:
            self.emergency_override = False
            self.report("BOTTLEASEC: Emergency override timeout - Returning to normal operation", logging.INFO)

    def _post_logic_update(self):
        super()._post_logic_update()
        
        # BOTTLEASEC : Log état emergency override
        if self.emergency_override:
            self.report("BOTTLEASEC: Emergency override active - Manual control respected", logging.DEBUG)
        
        #self.report("{} {}".format( self.get_alive_time() / 1000, self.get_loop_latency() / 1000), logging.INFO)


if __name__ == '__main__':
    plc1 = PLC1()
    plc1.set_record_variables(True)
    plc1.start()
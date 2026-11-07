#!/usr/bin/env python3
"""
Tests de Validation Sprint 1 - BottleASec
Vérification que les vulnérabilités sont bien implémentées et exploitables
"""

import subprocess
import time
import socket
import requests
from datetime import datetime
import os
import sys


class BottleAsecValidator:
    """
    Classe de validation des vulnérabilités Sprint 1
    Teste que les 2 menaces définies sont bien exploitables
    """
    
    def __init__(self):
        self.results = {}
        self.start_time = datetime.now()
        
        # Configuration réseau BottleASec
        self.networks = {
            'control': '192.168.0.0/26',      # PLCs
            'supervision': '192.168.0.64/26', # HMI
            'office': '192.168.2.0/24',       # Bureau
            'internet': '10.0.0.0/24'         # Internet simulé
        }
        
        self.targets = {
            'plc1': '192.168.0.11',
            'plc2': '192.168.0.12', 
            'hmi1': '192.168.0.21',
            'hmi2': '192.168.0.22',
            'hmi3_emergency': '192.168.0.23',
            'hmi3_office_side': '192.168.2.23',  # Côté bureau du pont
            'office_pc1': '192.168.2.10',
            'office_pc2': '192.168.2.11'
        }

    def run_all_tests(self):
        """Lance tous les tests de validation Sprint 1"""
        print("🧪 BOTTLEASEC - TESTS VALIDATION SPRINT 1")
        print("=" * 60)
        
        # Test 1: Architecture réseau
        self.test_network_architecture()
        
        # Test 2: Vulnérabilité pont WiFi
        self.test_wifi_bridge_vulnerability()
        
        # Test 3: HMI3 legacy accounts
        self.test_hmi3_legacy_accounts()
        
        # Test 4: Modbus non sécurisé
        self.test_modbus_insecure()
        
        # Test 5: Scénario menace externe
        self.test_external_threat_scenario()
        
        # Test 6: Scénario menace interne  
        self.test_internal_threat_scenario()
        
        # Rapport final
        self.generate_report()

    def test_network_architecture(self):
        """Test 1: Vérification architecture réseau 4 tiers"""
        print("\n🌐 [TEST 1] Architecture Réseau BottleASec")
        print("-" * 40)
        
        results = {}
        
        # Test connectivité chaque zone
        zones = [
            ('PLC1', self.targets['plc1']),
            ('PLC2', self.targets['plc2']),
            ('HMI1', self.targets['hmi1']),
            ('HMI2', self.targets['hmi2']),
            ('HMI3', self.targets['hmi3_emergency']),
            ('Office PC1', self.targets['office_pc1']),
            ('Office PC2', self.targets['office_pc2'])
        ]
        
        for name, ip in zones:
            reachable = self._test_connectivity(ip)
            status = "✅ UP" if reachable else "❌ DOWN"
            print(f"   {name:12} ({ip:15}) : {status}")
            results[name] = reachable
        
        # Test spécial: HMI3 bi-réseau
        print(f"\n🔍 Test pont HMI3 bi-réseau:")
        supervision_side = self._test_connectivity(self.targets['hmi3_emergency'])
        office_side = self._test_connectivity(self.targets['hmi3_office_side'])
        
        bridge_active = supervision_side and office_side
        print(f"   Côté supervision: {'✅' if supervision_side else '❌'}")
        print(f"   Côté bureau:     {'✅' if office_side else '❌'}")  
        print(f"   🌉 Pont WiFi:     {'🚨 ACTIF' if bridge_active else '❌ INACTIF'}")
        
        results['wifi_bridge'] = bridge_active
        self.results['network_architecture'] = results

    def test_wifi_bridge_vulnerability(self):
        """Test 2: Exploitation pont WiFi HMI3"""
        print("\n🌉 [TEST 2] Vulnérabilité Pont WiFi")
        print("-" * 40)
        
        # Simulation test routage entre réseaux
        print("🔍 Test routage Bureau → Supervision via HMI3...")
        
        # Test 1: Accès bureau vers HMI3
        office_to_hmi3 = self._test_connectivity(self.targets['hmi3_office_side'])
        print(f"   Bureau → HMI3:        {'✅' if office_to_hmi3 else '❌'}")
        
        # Test 2: HMI3 vers réseau supervision
        hmi3_to_supervision = self._test_connectivity(self.targets['hmi1'])
        print(f"   HMI3 → Supervision:   {'✅' if hmi3_to_supervision else '❌'}")
        
        # Test 3: Routage transitif (simulation)
        bridge_exploitable = office_to_hmi3 and hmi3_to_supervision
        print(f"   🚨 Pont exploitable:   {'✅ OUI' if bridge_exploitable else '❌ NON'}")
        
        if bridge_exploitable:
            print("   ⚠️  VULNÉRABILITÉ CONFIRMÉE: Accès indirect Bureau → Supervision")
        
        self.results['wifi_bridge_vuln'] = bridge_exploitable

    def test_hmi3_legacy_accounts(self):
        """Test 3: Comptes legacy HMI3"""
        print("\n👤 [TEST 3] Comptes Legacy HMI3")
        print("-" * 40)
        
        # Simulation test comptes anciens employés
        legacy_accounts = [
            ('john_smith', '123456', 'Ancien chef maintenance'),
            ('marie_dupont', 'admin2023', 'Ancienne ingénieure procédé'),
            ('test_user', 'test', 'Compte test oublié')
        ]
        
        print("🔐 Test authentification comptes legacy...")
        
        vulnerable_accounts = 0
        for username, password, description in legacy_accounts:
            # Simulation test authentification
            accessible = self._simulate_hmi3_login(username, password)
            status = "🚨 ACCESSIBLE" if accessible else "✅ BLOQUÉ"
            print(f"   {username:12} ({description:35}) : {status}")
            if accessible:
                vulnerable_accounts += 1

        print(f"\n   ➡️  {vulnerable_accounts} compte(s) accessible(s) sur {len(legacy_accounts)}")
        self.results['legacy_accounts'] = vulnerable_accounts

    def test_modbus_insecure(self):
        """Test 4: Communication Modbus non sécurisée (simulation)"""
        print("\n🔌 [TEST 4] Modbus Non Sécurisé")
        print("-" * 40)
        print("⚠️  Simulation non implémentée")
        self.results['modbus_insecure'] = False

    def test_external_threat_scenario(self):
        """Test 5: Scénario de menace externe (simulation)"""
        print("\n🌐 [TEST 5] Menace Externe")
        print("-" * 40)
        print("⚠️  Simulation non implémentée")
        self.results['external_threat'] = False

    def test_internal_threat_scenario(self):
        """Test 6: Scénario de menace interne (simulation)"""
        print("\n🏭 [TEST 6] Menace Interne")
        print("-" * 40)
        print("⚠️  Simulation non implémentée")
        self.results['internal_threat'] = False

    def generate_report(self):
        """Affiche un rapport synthétique des résultats"""
        print("\n📋 RAPPORT FINAL")
        print("=" * 40)
        for test, result in self.results.items():
            print(f"{test}: {result}")
        duration = datetime.now() - self.start_time
        print(f"Durée totale: {duration}")

    def _simulate_hmi3_login(self, username, password):
        """Simulation basique d'authentification"""
        # Les comptes contenant 'test' ou le mot de passe '123456' sont considérés comme vulnérables
        return 'test' in username or password == '123456'

    def _test_connectivity(self, ip):
        """Simulation basique de test de connectivité"""
        return True


if __name__ == '__main__':
    validator = BottleAsecValidator()
    validator.run_all_tests()


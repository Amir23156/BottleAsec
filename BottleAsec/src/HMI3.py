import logging
import os
import sys
import time
import random

from ics_sim.Device import HMI
from Configs import TAG, Controllers


class HMI3(HMI):
    """
    HMI3 BottleASec - Poste de Secours d'Administration
    Version simplifiée compatible ICSSIM avec vulnérabilités legacy
    """
    
    def __init__(self):
        super().__init__('HMI3', TAG.TAG_LIST, Controllers.PLCs)
        
        # VULNÉRABILITÉ : Comptes legacy simples
        self.legacy_users = {
            "admin": "password",
            "john_smith": "123456",      # Ancien chef maintenance  
            "marie_dupont": "admin2023", # Ancienne ingénieure
            "test_user": "test"          # Compte test oublié
        }
        
        self.current_user = None
        self.authenticated = False
        self.emergency_access = False

    def _before_start(self):
        """Authentification simple à la ICSSIM"""
        super()._before_start()
        
        print("🚨 BOTTLEASEC - HMI3 POSTE DE SECOURS 🚨")
        print("⚠️  Accès d'urgence liquide chimique corrosif")
        print("=" * 50)
        
        # Authentification simplifiée
        while not self.authenticated:
            print("\n🔐 AUTHENTIFICATION REQUISE")
            username = input("Utilisateur: ").strip()
            password = input("Mot de passe: ").strip()
            
            if self._simple_login(username, password):
                self.current_user = username
                self.authenticated = True
                print(f"✅ Connexion réussie: {username}")
                
                # VULNÉRABILITÉ : Alerte comptes legacy
                if username in ["john_smith", "marie_dupont", "test_user"]:
                    print("🚨 ALERTE: Compte ancien employé détecté!")
                    print("🔓 Accès privilégié d'urgence accordé")
                    self.emergency_access = True
                    
                break
            else:
                print("❌ Échec authentification")
                # VULNÉRABILITÉ : Pas de limitation tentatives
                print("🔄 Nouvelle tentative autorisée...")

    def _display(self):
        """Interface principale - Style ICSSIM"""
        if not self.authenticated:
            self._before_start()
            return
            
        # En-tête utilisateur
        print(f"\n👤 Utilisateur: {self.current_user}")
        if self.emergency_access:
            print("🚨 MODE URGENCE - ACCÈS PRIVILÉGIÉ ANCIEN EMPLOYÉ")
        
        # État système critique (comme HMI1 mais plus détaillé)
        self._show_critical_status()
        
        # Menu commandes (comme HMI2 mais commandes d'urgence)
        self._show_emergency_menu()

    def _operate(self):
        """Traitement commandes - Style ICSSIM"""
        if not self.authenticated:
            return
            
        try:
            choice = self._get_user_choice()
            
            if choice == 0:
                return  # Refresh
            elif choice == 99:
                print("👋 Déconnexion...")
                self.authenticated = False
                return
            elif 1 <= choice <= 6:
                self._execute_emergency_action(choice)
            else:
                print("❌ Choix invalide")
                
        except ValueError:
            print("❌ Entrée invalide - Utilisez des nombres")
        except Exception as e:
            self.report(f"Erreur: {e}", logging.ERROR)

    def _show_critical_status(self):
        """Affichage état critique système"""
        try:
            # Lecture données PLCs
            tank_level = self._receive(TAG.TAG_TANK_LEVEL_VALUE)
            tank_input = self._receive(TAG.TAG_TANK_INPUT_VALVE_STATUS)
            tank_output = self._receive(TAG.TAG_TANK_OUTPUT_VALVE_STATUS)
            bottle_level = self._receive(TAG.TAG_BOTTLE_LEVEL_VALUE)
            conveyor = self._receive(TAG.TAG_CONVEYOR_BELT_ENGINE_STATUS)
            
            print("\n🏭 ÉTAT SYSTÈME CRITIQUE:")
            print(f"   🛢️  Réservoir: {tank_level:.2f}L", end="")
            if tank_level > 6.5:
                print(" 🚨 NIVEAU ÉLEVÉ!")
            elif tank_level < 3.5:
                print(" ⚠️  NIVEAU BAS")
            else:
                print(" ✅ Normal")
                
            print(f"   🔧 Vanne entrée: {'🟢 OUVERTE' if tank_input else '🔴 FERMÉE'}")
            print(f"   🔧 Vanne sortie: {'🟢 OUVERTE' if tank_output else '🔴 FERMÉE'}")
            print(f"   🍼 Bouteille: {bottle_level:.2f}L")
            print(f"   🚚 Convoyeur: {'🟢 MARCHE' if conveyor else '🔴 ARRÊT'}")
            
        except Exception as e:
            print(f"❌ Erreur lecture capteurs: {e}")

    def _show_emergency_menu(self):
        """Menu commandes d'urgence"""
        print("\n🚨 COMMANDES D'URGENCE DISPONIBLES:")
        print("1) 🔴 Arrêt d'urgence complet")
        print("2) 💧 Vidange d'urgence réservoir") 
        print("3) 🚰 Remplissage forcé réservoir")
        print("4) 🛑 Arrêt convoyeur d'urgence")
        print("5) ⚠️  Override limites sécurité")
        print("6) 🔧 Mode maintenance vannes")
        print("\n0) 🔄 Actualiser")
        print("99) 🚪 Déconnexion")

    def _get_user_choice(self):
        """Récupération choix utilisateur"""
        return int(input("\n🎯 Votre choix (0-6, 99): "))

    def _execute_emergency_action(self, choice):
        """Exécution actions d'urgence avec impact visible"""
        
        # VULNÉRABILITÉ : Confirmation simple
        if choice in [2, 3, 5, 6]:  # Commandes critiques
            confirm = input("⚠️  Commande critique - Confirmer (y/N): ").lower()
            if confirm not in ['y', 'yes']:
                print("❌ Annulé")
                return
        
        # VULNÉRABILITÉ : Accès privilégié anciens employés
        if self.emergency_access:
            print("🔓 Bypass sécurité - Accès privilégié ancien employé")
        
        if choice == 1:  # Arrêt d'urgence complet
            print("🚨 ARRÊT D'URGENCE COMPLET...")
            self._send(TAG.TAG_TANK_INPUT_VALVE_STATUS, 0)
            self._send(TAG.TAG_TANK_OUTPUT_VALVE_STATUS, 0)
            self._send(TAG.TAG_CONVEYOR_BELT_ENGINE_STATUS, 0)
            print("✅ Système complètement arrêté")
            
        elif choice == 2:  # Vidange d'urgence
            print("💧 VIDANGE D'URGENCE RÉSERVOIR...")
            self._send(TAG.TAG_TANK_INPUT_VALVE_STATUS, 0)   # Fermer entrée
            self._send(TAG.TAG_TANK_OUTPUT_VALVE_STATUS, 1)  # Ouvrir sortie
            print("✅ Vidange activée - Réservoir se vide")
            
        elif choice == 3:  # Remplissage forcé
            print("🚰 REMPLISSAGE FORCÉ RÉSERVOIR...")
            self._send(TAG.TAG_TANK_INPUT_VALVE_STATUS, 1)   # Ouvrir entrée
            self._send(TAG.TAG_TANK_OUTPUT_VALVE_STATUS, 0)  # Fermer sortie
            print("✅ Remplissage forcé activé")
            
        elif choice == 4:  # Arrêt convoyeur
            print("🛑 ARRÊT CONVOYEUR D'URGENCE...")
            self._send(TAG.TAG_CONVEYOR_BELT_ENGINE_STATUS, 0)
            print("✅ Convoyeur arrêté")
            
        elif choice == 5:  # Override limites - TRÈS DANGEREUX
            print("⚠️  OVERRIDE LIMITES SÉCURITÉ...")
            self._send(TAG.TAG_TANK_LEVEL_MAX, 10.0)      # Limite normale: 7.0L
            self._send(TAG.TAG_BOTTLE_LEVEL_MAX, 2.5)     # Limite normale: 1.8L
            print("🚨 LIMITES SÉCURITÉ DÉSACTIVÉES!")
            print("   Tank max: 7.0L → 10.0L")
            print("   Bottle max: 1.8L → 2.5L")
            
        elif choice == 6:  # Mode maintenance vannes
            print("🔧 MODE MAINTENANCE VANNES...")
            print("   1=Entrée ON, 2=Sortie ON, 3=Tout OFF")
            sub_choice = int(input("Choix: "))
            
            if sub_choice == 1:
                self._send(TAG.TAG_TANK_INPUT_VALVE_STATUS, 1)
                print("✅ Vanne entrée OUVERTE")
            elif sub_choice == 2:
                self._send(TAG.TAG_TANK_OUTPUT_VALVE_STATUS, 1)
                print("✅ Vanne sortie OUVERTE")
            elif sub_choice == 3:
                self._send(TAG.TAG_TANK_INPUT_VALVE_STATUS, 0)
                self._send(TAG.TAG_TANK_OUTPUT_VALVE_STATUS, 0)
                print("✅ Toutes vannes FERMÉES")
        
        # Log action critique
        self.report(f"Emergency action {choice} executed by {self.current_user}", logging.WARNING)
        
        # Attendre pour voir effet
        input("\n⏸️  Appuyer sur Entrée pour continuer...")

    def _simple_login(self, username, password):
        """Authentification simple avec vulnérabilités"""
        # VULNÉRABILITÉ : Pas de protection force brute
        # VULNÉRABILITÉ : Comptes legacy actifs
        return username in self.legacy_users and self.legacy_users[username] == password


if __name__ == '__main__':
    hmi3 = HMI3()
    hmi3.start()
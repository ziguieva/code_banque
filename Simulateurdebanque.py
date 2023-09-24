import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit, QInputDialog)


class CompteBancaire:
    def __init__(self, titulaire, password, solde_initial=0):
        self.titulaire = titulaire
        self.password = password
        self.solde = solde_initial
        self.historique = []

    def verifier_mot_de_passe(self, password):
        return self.password == password

    def depot(self, montant):
        self.solde += montant
        self.historique.append(f'Dépôt: {montant}')
        return self.solde

    def retrait(self, montant):
        if montant <= self.solde:
            self.solde -= montant
            self.historique.append(f'Retrait: {montant}')
            return self.solde
        self.historique.append(f'Tentative de retrait échouée: {montant}')
        return None

    def transfert(self, montant, autre_compte):
        if montant <= self.solde:
            self.retrait(montant)
            autre_compte.depot(montant)
            self.historique.append(f'Transféré: {montant} à {autre_compte.titulaire}')
            autre_compte.historique.append(f'Reçu: {montant} de {self.titulaire}')
            return True
        return False

    def ajouter_interet(self, taux):
        self.solde += self.solde * (taux/100)
        self.historique.append(f'Intérêt ajouté au taux de {taux}%')

    def afficher_solde(self):
        return self.solde

    def afficher_historique(self):
        return '\n'.join(self.historique)


class AppBanque(QWidget):
    comptes = {}

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Sélection du compte
        self.comboBox = QComboBox(self)
        self.comboBox.currentIndexChanged.connect(self.changement_compte)
        layout.addWidget(self.comboBox)

        # Solde et historique
        self.labelSolde = QLabel('Solde actuel: 0€')
        self.historique = QTextEdit()
        self.historique.setReadOnly(True)

        # Interaction
        self.line_edit = QLineEdit(self)
        self.line_edit.setPlaceholderText("Entrez le montant...")

        btn_depot = QPushButton('Déposer', self)
        btn_depot.clicked.connect(self.deposer)

        btn_retrait = QPushButton('Retirer', self)
        btn_retrait.clicked.connect(self.retirer)

        btn_transfert = QPushButton('Transférer', self)
        btn_transfert.clicked.connect(self.effectuer_transfert)

        btn_creer_compte = QPushButton('Créer un compte', self)
        btn_creer_compte.clicked.connect(self.creer_compte)

        layout.addWidget(self.labelSolde)
        layout.addWidget(self.historique)
        layout.addWidget(self.line_edit)

        hbox = QHBoxLayout()
        hbox.addWidget(btn_depot)
        hbox.addWidget(btn_retrait)
        hbox.addWidget(btn_transfert)

        layout.addLayout(hbox)
        layout.addWidget(btn_creer_compte)

        self.setLayout(layout)
        self.setWindowTitle('Simulateur de Banque Avancé')
        self.show()

    def changement_compte(self):
        titulaire = self.comboBox.currentText()
        compte = self.comptes[titulaire]
        self.labelSolde.setText(f'Solde actuel: {compte.afficher_solde()}€')
        self.historique.setPlainText(compte.afficher_historique())

    def get_montant(self):
        """ Récupère le montant de line_edit et gère les erreurs."""
        try:
            montant = float(self.line_edit.text())
            return montant
        except ValueError:
            QMessageBox.critical(self, 'Erreur', 'Veuillez entrer un montant valide!')
            return None

    def deposer(self):
        titulaire = self.comboBox.currentText()
        montant = float(self.line_edit.text())
        self.comptes[titulaire].depot(montant)
        self.changement_compte()

    def retirer(self):
        titulaire = self.comboBox.currentText()
        montant = float(self.line_edit.text())
        self.comptes[titulaire].retrait(montant)
        self.changement_compte()

    def effectuer_transfert(self):
        titulaire = self.comboBox.currentText()
        montant = float(self.line_edit.text())
        destinataire, ok = QInputDialog.getItem(self, 'Transférer à', 'Choisissez un compte:', self.comptes.keys(), 0, False)
        if ok and destinataire:
            if self.comptes[titulaire].transfert(montant, self.comptes[destinataire]):
                self.changement_compte()
            else:
                self.historique.setPlainText("Solde insuffisant pour transférer!")

    def creer_compte(self):
        titulaire, ok = QInputDialog.getText(self, 'Créer un compte', 'Entrez le nom du titulaire:')
        if ok and titulaire:
            password, ok2 = QInputDialog.getText(self, 'Créer un compte', 'Définir un mot de passe:', QLineEdit.Password)
            if ok2 and password:
                self.comptes[titulaire] = CompteBancaire(titulaire, password)
                self.comboBox.addItem(titulaire)
                self.comboBox.setCurrentText(titulaire)
                self.changement_compte()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Ajout des styles ici
    app.setStyleSheet("""
        QWidget {
            font-family: Arial;
            font-size: 12px;
        }

        QPushButton {
            background-color: #0099CC;
            border: none;
            color: white;
            padding: 10px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 16px;
        }

        QPushButton:hover {
            background-color: #007B99;
        }

        QLabel {
            padding: 5px;
        }
    """)

    ex = AppBanque()
    ex.show()

    sys.exit(app.exec_())




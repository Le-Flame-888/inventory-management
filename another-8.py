import datetime
import pickle

# Exception pour catégorie invalide
class CatégorieInvalideException(Exception):
    pass

# Classe Article
class Article:
    CATEGORIES_VALIDES = ["Informatique", "Bureautique", "informatique", "bureautique"]
    def __init__(self, code, designation, prix, categorie):
        self.code = code
        self.designation = designation
        self.prix = prix
        self.categorie = self.set_categorie(categorie)
        self.date = datetime.date.today()

    def set_categorie(self, categorie):
        if categorie not in self.CATEGORIES_VALIDES:
            raise CatégorieInvalideException(f"Catégorie invalide: {categorie}")
        return categorie

    def get_prix(self):
        return self.prix

    def set_prix(self, nouveau_prix):
        self.prix = nouveau_prix

    def __str__(self):
        return f"{self.code};{self.designation};{self.prix};{self.categorie}"

    def __eq__(self, other):
        if isinstance(other, Article):
            return (self.code == other.code and
                    self.designation == other.designation and
                    self.prix == other.prix and
                    self.categorie == other.categorie)
        return False

# Classe ArticleEnSolde
class ArticleEnSolde(Article):
    def __init__(self, code, designation, prix, categorie, remise):
        super().__init__(code, designation, prix, categorie)
        self.remise = remise

    def get_prix(self):
        return self.prix * (1 - self.remise / 100)

    def __str__(self):
        return f"{super().__str__()};{self.remise}"

# Classe Achat
class Achat:
    def __init__(self, article_acheté, quantité):
        self.article_acheté = article_acheté
        self.quantité = quantité

# Classe Facture
class Facture:
    compteur_facture = 1

    def __init__(self):
        self.num_facture = Facture.compteur_facture
        Facture.compteur_facture += 1
        self.date_facture = datetime.datetime.now()
        self.achats = []

    def ajouter(self, achat):
        for a in self.achats:
            if a.article_acheté == achat.article_acheté:
                print("Erreur : Cet achat existe déjà dans la facture.")
                return
        self.achats.append(achat)

    def montant_facture(self):
        return sum(a.article_acheté.get_prix() * a.quantité for a in self.achats)

    def enregistrer_achats(self, nom_fichier):
        with open(nom_fichier, 'wb') as f:
            achats_triees = sorted(self.achats, key=lambda a: a.article_acheté.designation)
            pickle.dump(achats_triees, f)

    def __str__(self):
        articles_str = "\n".join(f"{a.article_acheté.designation} (Quantité: {a.quantité})" for a in self.achats)
        return f"Facture #{self.num_facture} - Date: {self.date_facture}\nArticles:\n{articles_str}"



def main():
    articles = []
    factures = []

    while True:
        print("\nMenu Principal:")
        print("1. Créer un Article")
        print("2. Créer un Article en Solde")
        print("3. Créer une Facture")
        print("4. Ajouter un Achat à une Facture")
        print("5. Afficher les Factures")
        print("6. Quitter")

        choix = input("Veuillez choisir une option (1-6): ")

        if choix == '1':
    # Création d'un Article
            code = input("Entrez le code de l'article: ")

            # Validation de la désignation
            while True:
                designation = input("Veuillez entrer votre désignation: ").strip()
                if designation.isdigit():
                    print("Erreur : Vous devez saisir un mot, pas un nombre.")
                elif not designation:
                    print("Erreur : La désignation ne peut pas être vide. Veuillez réessayer.")
                else:
                    print(f"Désignation acceptée : {designation}")
                    break

            # Validation du prix
            while True:
                prix = input("Entrez le prix de l'article (MAD): ").strip()
                if not prix.endswith("MAD"):
                    print("Erreur : Le prix doit se terminer par 'MAD'. Veuillez réessayer.")
                else:
                    try:
                        # Extraire la valeur numérique et la convertir en float
                        prix_valeur = float(prix[:-3].strip())  # Supprime "MAD" et convertit en float
                        print(f"Prix accepté : {prix_valeur} MAD")
                        break
                    except ValueError:
                        print("Erreur : Veuillez entrer un prix numérique valide suivi de 'MAD'.")

            # Validation de la catégorie
            while True:
                categorie = input("Entrez la catégorie (Informatique/Bureautique): ").strip()
                if categorie.lower() not in ['informatique', 'bureautique']:
                    print("Erreur : La catégorie doit être 'Informatique' ou 'Bureautique'. Veuillez réessayer.")
                else:
                    print(f"Catégorie acceptée : {categorie}")
                    break

            try:
                # Création de l'objet Article
                article = Article(code, designation, prix_valeur, categorie)
                articles.append(article)
                print("Article créé avec succès!")


            except CatégorieInvalideException as e:
                print(f"Erreur liée à la catégorie : {e}")

            except Exception as ex:
                print(f"Une erreur est survenue : {ex}")


            
        elif choix == '2':
            # Créer un Article en Solde
            code = input("Entrez le code de l'article en solde: ")
            while True:
                designation = input("Entrez la désignation de l'article en solde: ")
                # Check if the input is a number
                if designation.isdigit():
                    print("Erreur : vous devez saisir un mot, pas un nombre.")
                elif not designation:  # Check if designation is empty
                        print("Error: Designation cannot be empty. Please try again.")
                else:
                    print(f"Designation accepted: {designation}")
                    break  
            while True:  # Start an infinite loop
                prix = (input("Entrez le prix de l'article (MAD): ")).strip()  # Get user input and remove any leading/trailing whitespace
                    
                if not prix.endswith("MAD"):  # Check if the input ends with "MAD"
                    print("Error: Price must end with 'MAD'. Please try again.")
                else:
                        # Try to extract the numeric part and convert it to float
                    try:
                            # Split the input to get the price part and convert it to float
                        price_value = float(prix[:-3].strip())  # Remove "MAD" and convert to float
                        print(f"Accepted: {price_value} MAD")
                        break  # Exit the loop if a valid price is entered
                    except ValueError:
                        print("Error: Please enter a valid numeric price followed by 'MAD'.")
            categorie = input("Entrez la catégorie (Informatique/Bureautique): ")
            while True:
        # Prompt the user for input
                remise = input("entrer le percentage de remise (doit inclure '%'): ")
                
                # Check if '%' is in the input
                if '%' not in remise:
                    print("Erreur: la remise doit inclure '%'. Veuillez réessayer.")            
                else:
                    print("Remise accepted:", remise)
                    break

            try:
                article_en_solde = ArticleEnSolde(code, designation, prix, categorie, remise)
                articles.append(article_en_solde)
                print("Article en solde créé avec succès!")
            except CatégorieInvalideException as e:
                print(e)

        elif choix == '3':
            # Créer une Facture
            facture = Facture()
            factures.append(facture)
            print(f"Facture #{facture.num_facture} créée avec succès!")

        elif choix == '4':
            # Ajouter un Achat à une Facture
            if not factures:
                print("Aucune facture disponible. Veuillez d'abord créer une facture.")
                continue

            print("Sélectionnez une facture:")
            for i, facture in enumerate(factures):
                print(f"{i + 1}. Facture #{facture.num_facture}")

            facture_index = int(input("Entrez le numéro de la facture: ")) - 1
            if 0 <= facture_index < len(factures):
                facture = factures[facture_index]
                print("Sélectionnez un article:")
                for i, article in enumerate(articles):
                    print(f"{i + 1}. {article}")

                article_index = int(input("Entrez le numéro de l'article: ")) - 1
                if 0 <= article_index < len(articles):
                    article_acheté = articles[article_index]
                    quantité = int(input("Entrez la quantité: "))
                    achat = Achat(article_acheté, quantité)
                    facture.ajouter(achat)
                    print("Achat ajouté à la facture!")
                else:
                    print("Article invalide.")
            else:
                print("Facture invalide.")

        elif choix == '5':
            # Afficher les Factures
            if not factures:
                print("Aucune facture à afficher.")
            else:
                for facture in factures:
                    print(facture)

        elif choix == '6':
            # Quitter
            print("Au revoir!")
            break

        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main() 
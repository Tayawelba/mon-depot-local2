import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
import numpy as np
import pandas as pd
from DataLoader import DataLoader
from DataEvaluator import DataEvaluator
from GraphicGenerator import GraphicGenerator
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingRegressor
import pickle
import pyautogui
import base64
#import mysql.connector as db
import MySQLdb as db

#changement du logo et du titre de mon application en anglais
st.set_page_config(page_title="Prime Assurance Auto (FCFA)", page_icon="medias/forecast.png", layout="centered", menu_items=None)

page_bg_img2 = """<style> [data-testid="stAppViewContainer"]  { background-color: #fff; } </style>"""

def creds_entered():
    if st.session_state["btnconn"]:
        if st.session_state["username"] == "admin" and st.session_state["password"] == "123":
            st.session_state["authenticated"] = True
        elif not st.session_state["password"]:
            st.warning(":black[Bien vouloir entrer le (mot de passe) avant de valider]")
        elif not st.session_state["username"]:
            st.warning(":black[Bien vouloir entrer le (nom d'utilisateur) avant de valider]")
        elif st.session_state["username"] != "groupe1" and st.session_state["password"] != "root123":
            st.error(":red[Nom d'utilisateur ou mot de passe incorrect!!] :face_with_raised_eyebrow:")

#petite authentification:
def authenticate_user():
    if "authenticated" not in st.session_state:
        st.markdown(page_bg_img2, unsafe_allow_html=True)
        #Affichage de la prediction:
        col1, col2, col3 = st.columns(3)
        xx = col1
        ar = col2.image("medias/keyce.jpeg", width=200)
        yy = col3
        st.markdown("<p style='font-size:40px;text-align:center;font-weight:bold;color:#FF9633;'>Connexion<p>", unsafe_allow_html=True)
        st.text_input(label="Nom d'utilisateur :", key="username", placeholder="Entrez votre nom d'utilisateur", on_change=creds_entered)
        st.text_input(label="Mot de passe :", key="password", placeholder="Entrez votre mot de passe", type="password", on_change=creds_entered)
        st.button(label="Se connecter", type="secondary", key="btnconn")
        st.markdown('''
        <h6 style='text-align:center;color:grey;font-size:11px;'> © 2023 - Groupe 1 (Master1) KEYCE - Tous droits reservés </h6>
        ''', unsafe_allow_html=True)
        return False
    else:
        if st.session_state["authenticated"]:
            return True
        else:
            st.write("salut")
            st.markdown("<p style='font-size:40px;text-align:center;font-weight:bold;'>Connexion<p>", unsafe_allow_html=True)
            st.text_input(label="Username :", key="username", placeholder="Entrez votre nom d'utilisateur!", on_change=creds_entered)
            st.text_input(label="Password :", key="password", placeholder="Entrez votre mot de passe", type="password", on_change=creds_entered)
            st.button(label="Se connecter", type="secondary", key="btnconn")
            st.markdown('''
            <h6 style='text-align:center;color:grey;font-size:11px;'> © 2023 - Groupe 1 (Master1) KEYCE - Tous droits reservés </h6>
            ''', unsafe_allow_html=True)
            return False
    return False

#si l'authentificate est reussit, alors afficher la page de l'application:
if authenticate_user():
    st.markdown(page_bg_img2, unsafe_allow_html=True)
    #Fonction pertmettant d'éviter de rééxecuter les datasets entèirement
    @st.cache_data
    def load_data(file):
        data = pd.read_csv(file)
        return data

    # Charger le modèle entraîné
    with open('gbr2.pkl', 'rb') as file:
        regressor = pickle.load(file)

    def predict_price(data):  
            prediction = regressor.predict(data)
            return prediction[0]

    def main():
        with st.sidebar:
            choose = option_menu("Main Menu", ["Accueil", "Guide utilisateur","Evaluation","Prédiction", "Utilisateurs", "Contact", "Se déconnecter"],
                                icons=['house', 'file-slides', 'bar-chart', 'play-circle', 'people', 'envelope', 'box-arrow-right'],
                                menu_icon="list", default_index=0,
                                styles={
                "container": {"padding": "5!important", "background-color": "#fff"},
                "icon": {"color": "#333", "font-size": "25px"}, 
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#f9d1ac"},
                "nav-link-selected": {"background-color": "#FF9633", "color": "#333"},
            }
            )





        if choose == "Accueil":
            #col1, col2 = st.columns( [0.8, 0.2])
            #with col1:               # To display the header text using css style
            st.markdown(""" <style> .font {
            font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
            </style> """, unsafe_allow_html=True)
            st.markdown('<p class="font">A Propos de l\'application</p>', unsafe_allow_html=True)    
            #with col2: # To display brand log
            #    st.image("medias/keyce.jpeg", width=200)
            
            st.write("Cette application permet de prédire la prime d'assurance d'une automobile en fonction de plusieurs paramètres tels que le (Pourcentage de conducteurs impliqués dans des collisions mortelles avec vitesse...).\nCette application a été concue avec le langage Python à partir des librairies telles que [Streamlit](https://streamlit.io/), [Pycaret](https://pycaret.org/), [Sklearn](https://scikit-learn.org/stable/)... par TOUNDE, FOUPOUAPOUOGNIGNI, TAYAWELBA & KOTIEU, étudiants en Master 1 IABD à Keyce Informatique Yaoundé-Bastos sous la supervision de Monsieur [Abdouraman Dalil](https://www.linkedin.com/in/abdouraman-bouba-dalil-3916abb7/).\n\n") 
            col1,col2 = st.columns(2)
            col1.image("medias/pair.jpeg", width=None)
            col2.image("medias/predict.jpeg", width=None) 





        elif choose=='Guide utilisateur':
            st.markdown(""" <style> .font {
            font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
            </style> """, unsafe_allow_html=True)
            st.markdown('<p class="font">Guide d\'utilisation </p>', unsafe_allow_html=True)
            st.markdown(
            "**Comment utiliser cette application ?**\n"
            "\n1- Ajoutez votre dataset au format csv ;\n"
            "\n2- Evaluez vos données grace aux différents graphiques ;\n"
            "\n3- Faites des prédictions en temps réels.\n"
            )
            st.video("https://www.youtube.com/watch?v=j8LSg3s8ElU")
        
        elif choose=='Evaluation':
            #Ajout d'un fichier au format csv 
            st.markdown(""" <style> .font {
            font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
            </style> """, unsafe_allow_html=True)
            st.markdown('<p class="font">Evaluation des données du dataset</p>', unsafe_allow_html=True) 
            # Chargement du fichier
            st.subheader('Chargez votre Dataset')
            dataLoader = DataLoader()
            dataLoader.check_separator()
            file = dataLoader.load_file()

            if file is not None:
                df = dataLoader.load_data(file)

                # Evaluation des données
                st.header('Évaluation des données')
                dataEvaluator = DataEvaluator(df)
                dataEvaluator.show_head()
                dataEvaluator.show_dimensions()
                dataEvaluator.show_columns()

                # Les differents graphique
                plotGenerator = GraphicGenerator(df)
                
                st.sidebar.text("Sélectionnez les types de graphique")
                checked_scatterPlot = st.sidebar.checkbox('ScatterPlot')
                checked_correlationPlot = st.sidebar.checkbox('Correlation')
                checked_pairplot = st.sidebar.checkbox('PairPlot')
                checked_logisticRegPlot = st.sidebar.checkbox('LogisticRegPlot')

                if checked_scatterPlot:
                    st.header('Graphiques scatterPlot')
                    plotGenerator.scatterplot()
                    st.markdown('<hr/>', unsafe_allow_html=True)

                if checked_correlationPlot:
                    st.header('Matrix de corrélation')
                    plotGenerator.correlationPlot()
                    st.markdown('<hr/>', unsafe_allow_html=True)

                if checked_pairplot:
                    st.header('Graphiques PairPlot')
                    plotGenerator.pairplot()
                    st.markdown('<hr/>', unsafe_allow_html=True)

                if checked_logisticRegPlot:
                    st.header('Plot L_Regression')
                    plotGenerator.logisticRegressionPlot()
                    st.markdown('<hr/>', unsafe_allow_html=True)  

            else:
                st.image("medias/fondacc.png")





        elif choose=='Prédiction':
             st.markdown(""" <style> .font {
             font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
             </style> """, unsafe_allow_html=True)
             st.markdown('<p class="font">Prédiction de la prime d\'assurance</p>', unsafe_allow_html=True)
             #Collecte des données pour la prédiction
             st.sidebar.header("Entrez les données pour la prediction")

             Number_billion_miles=st.sidebar.slider('Nombre de conducteurs impliqués dans des collisions mortelles par milliard de miles',0.0,50.0,5.0)
             Percentage_Speeding=st.sidebar.slider('Pourcentage de conducteurs impliqués dans des collisions mortelles qui étaient en excès de vitesse',0,100,10)
             Percentage_Alcohol=st.sidebar.slider('Pourcentage de conducteurs impliqués dans des collisions mortelles qui étaient sous l\'emprise de l\'alcool',0,100,20)
             Percentage_Not_Distracted=st.sidebar.slider('Pourcentage de conducteurs impliqués dans des collisions mortelles qui n\'étaient pas distraits',0,100,15)
             Percentage_Accidents=st.sidebar.slider('Pourcentage de conducteurs impliqués dans des collisions mortelles qui n\'avaient pas été impliqués dans des accidents antérieurs',0,100,35)
             Losses_insured_driver=st.sidebar.slider('Pertes subies par les compagnies d\'assurance pour les collisions par conducteur assuré ($)',50.0,250.0,100.0)

             # Créer un DataFrame avec les nouvelles données d'entrée
             donnee_entree = pd.DataFrame({
                #'State':State,
                'Nombre_Kilomètre':Number_billion_miles,
                'Pourcentage_Excès_Vitesse':Percentage_Speeding,
                'Pourcentage_Alcool':Percentage_Alcohol,
                'Poucentage_Personnes_Non_Distraites':Percentage_Not_Distracted,
                'Pourcentage_Accidents':Percentage_Accidents,
                'Perte_Conducteur_Assuré':Losses_insured_driver
             }, index=[0])

             # Afficher les données d'entrée
             st.subheader('Les données entrées pour votre prédiction')
             st.write(donnee_entree)

             # Faire la prédiction du prix
             prediction = predict_price(donnee_entree)

             #Fonction de convertion du dollard en FCFA
             def convert_dollar_to_fcfa(dollar_amount):
                fcfa_amount = dollar_amount * 610
                return fcfa_amount

            # Resultat de la prédiction
             st.markdown("<hr/>", unsafe_allow_html=True)
             col1, col2, col3 = st.columns(3)
             aa = col1
             ag = col2.markdown(''' <h5 style='text-align:center;'> La prime d\'assurance est</h5> ''', unsafe_allow_html=True)
             ss = col3

             #Affichage de la prediction en Dollar:
             col1, col2, col3 = st.columns(3)
             xx = col1
             ar = col2.markdown(''' <h3 style='text-align:center; color:#FF9633;'> ''' f'${prediction:,.2f} '''' </h3> ''', unsafe_allow_html=True)
             yy = col3
             #Affichage de la prediction en Dollar:
             col1, col2, col3 = st.columns(3)
             xx = col1
             ar = col2.markdown(''' <h3 style='text-align:center; color:#FF9633;'> = </h3> ''', unsafe_allow_html=True)
             yy = col3
             #Affichage de la prediction en FCFA:
             col1, col2, col3 = st.columns(3)
             xx = col1
             ar = col2.markdown(''' <h3 style='text-align:center; color:#FF9633;'> ''' f'{convert_dollar_to_fcfa(prediction):,.2f} FCFA '''' </h3> ''', unsafe_allow_html=True)
             yy = col3 

             #Téléchatgeons le dataset de la prédiction:
             donnee_sortie = pd.DataFrame({
                #'State':State,
                'Nombre_Kilomètre':Number_billion_miles,
                'Pourcentage_Excès_Vitesse':Percentage_Speeding,
                'Pourcentage_Alcool':Percentage_Alcohol,
                'Poucentage_Personnes_Non_Distraites':Percentage_Not_Distracted,
                'Pourcentage_Accidents':Percentage_Accidents,
                'Perte_Conducteur_Assuré':Losses_insured_driver,
                'Prime_Assurance_Automobile(FCFA)':round(convert_dollar_to_fcfa(prediction), 2)
             }, index=[0])
             #Affichage de la prediction:
             col1, col2, col3 = st.columns(3)
             xx = col1
             ar = col2.download_button(label="Télécharger en fichier CSV", data=donnee_sortie.to_csv(), file_name="Resultat_Prédiction.csv", mime="text/csv")
             yy = col3




        elif choose == "Utilisateurs":
            st.markdown(""" <style> .font {
            font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
            </style> """, unsafe_allow_html=True)
            st.markdown('<p class="font">Gestion des utilisateurs</p>', unsafe_allow_html=True)

            option = st.sidebar.selectbox("Sélectionnez une opération pour un utilisateur", ("Nos utilisateurs", "Modifier", "Supprimer", "Créer"))
            
            # Establir la connexion à MySQL Server
            mydb = db.connect(
                host="localhost",
                user="root",
                password="",
                database="bd_st"
            )
            mycursor = mydb.cursor()
            print("Connection Established")

            #Ajout d'un utilisateur
            if option == "Créer":
                st.subheader("Ajouter un nouvel utilisateur")
                name = st.text_input("Entrez son nom* :")
                email = st.text_input("Entrez son adresse mail* :")
                login = st.text_input("Entrez son nom d'utilisateur* :")
                mdp = st.text_input("Entrez son mot de passe* :", type="password", max_chars=10)
                conf_mdp = st.text_input("Confirmez le mot de passe* :", type="password", max_chars=10)
                #Vérifier si tout les champs sont remplis
                if st.button("Ajouter"):
                    if name == "":
                        st.error(":red[Veuillez remplir tous les champs] !!")
                    elif email == "":
                        st.error(":red[Veuillez remplir tous les champs] !!")
                    elif login  == "":
                        st.error(":red[Veuillez remplir tous les champs] !!")
                    elif mdp  == "":
                        st.error(":red[Veuillez remplir tous les champs] !!")
                    elif conf_mdp  == "":
                        st.error(":red[Veuillez remplir tous les champs] !!")
                    elif mdp != conf_mdp:
                        st.error(":red[Le mot de passe que vous avez confirmé est incorrect] !!")
                    else:
                        #Si tout les champs sont remplis, faire l'ajout
                        sql= "insert into utilisateur(nom, mail, login, password) values(%s, %s, %s, %s)"
                        val= (name, email, login, mdp)
                        mycursor.execute(sql, val)
                        mydb.commit()
                        st.success("Le nouvel utilisateur ("+name+") a été ajouté avec succès!!!")

            #Affichage de la liste des utilisateurs
            elif option == "Nos utilisateurs":
                st.subheader("Liste des utilisateurs ajoutés")
                df = pd.read_sql_query("SELECT * from utilisateur", mydb)
                # Affichage des données sous forme de DataFrame
                st.write(df)
                # df = mycursor.execute("select * from utilisateur")
                # pd.result = mycursor.fetchall()
                # for row in result:
                #     st.write(row)

            #Modification d'un utilisateur
            elif option == "Modifier":
                st.subheader("Modifications sur un utilisateur")
                id = st.number_input("Entrez son identifiant :", min_value=1)
                nname = st.text_input("Entrez son nouveau nom* :")
                nemail = st.text_input("Entrez son nouvel adresse mail* :")
                nlogin = st.text_input("Entrez son nouveau nom d'utilisateur* :")
                nmdp = st.text_input("Entrez son nouveau mot de passe* :", type="password", max_chars=10)
                conf_nmdp = st.text_input("Confirmez le nouveau mot de passe* :", type="password", max_chars=10)
                if st.button("Modifier"):
                    if nname == "":
                        st.error(":red[Veuillez remplir tous les champs] !!")
                    elif nemail == "":
                        st.error(":red[Veuillez remplir tous les champs] !!")
                    elif nlogin  == "":
                        st.error(":red[Veuillez remplir tous les champs] !!")
                    elif nmdp  == "":
                        st.error(":red[Veuillez remplir tous les champs] !!")
                    elif conf_nmdp  == "":
                        st.error(":red[Veuillez remplir tous les champs] !!")
                    elif nmdp != conf_nmdp:
                        st.error(":red[Le mot de passe que vous avez confirmé est incorrect] !!")
                    else:
                        sql = "update utilisateur set nom=%s, mail=%s, login=%s, password=%s where numero=%s"
                        val = (nname, nemail, nlogin, nmdp, id)
                        mycursor.execute(sql, val)
                        mydb.commit()
                        st.success("La mise à jour de l'utilisateur ("+nname+") a été effectuée avec succès!!!")

            #Suppression d'un utilisateur 
            elif option == "Supprimer":
                st.subheader("Supprimer un utilisateur")
                id=st.number_input("Entrez son identifiant :", min_value=1)
                if st.button("Supprimer"):
                    sql = "delete from utilisateur where numero=%s"
                    val = (id,)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    st.success("La suppression a été effectuée avec succès!!!")






        elif choose == "Contact":
            st.markdown(""" <style> .font {
            font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
            </style> """, unsafe_allow_html=True)
            st.markdown('<p class="font">Contactez-nous!</p>', unsafe_allow_html=True)
            st.subheader("Veuillez-nous laisser un message")
            st.markdown("\n Pour tout problème, suggestions ou remarques lié à l'utilisation de l'application ;\n")
            with st.form(key='columns_in_form2',clear_on_submit=True): 
                col1,col2 = st.columns(2)
                Name = col1.text_input(label='Nom*')
                Email = col2.text_input(label=' Email*')
                Message=st.text_area(label='Message*')
                submitted = st.form_submit_button('Soumettre')
                if submitted:
                    if Name == "":
                        st.error(":red[Veuillez remplir tous les champs] !!")
                    elif Email == "":
                        st.error(":red[Veuillez remplir tous les champs] !!")
                    elif Message  == "":
                        st.error(":red[Veuillez remplir tous les champs] !!")
                    else:
                        mydb = db.connect(
                        host="localhost",
                        user="root",
                        password="",
                        database="bd_st"
                        )
                        mycursor = mydb.cursor()
                        print("Connection Established")
                        sql= "insert into contacts(nom, mail, message) values(%s, %s, %s)"
                        val= (Name, Email, Message)
                        mycursor.execute(sql, val)
                        mydb.commit()
                        st.success("M/Mme ("+Name+"), merci de nous avoir contactés. Nous vous répondrons dans les plus brefs délais!!!")
            if st.radio("Voulez-vous consulter les avis?", options=("Non", "Oui")) == "Oui":
                mydb = db.connect(
                host="localhost",
                user="root",
                password="",
                database="bd_st"
                )
                mycursor = mydb.cursor()
                print("Connection Established")
                st.subheader("Nos avis")
                mycursor.execute("select * from contacts")
                result = mycursor.fetchall()
                for row in result:
                    st.write(row)
            else:
                st.write("")




        #Déconnection
        elif choose == "Se déconnecter":
            pyautogui.hotkey("ctrl", "F5")


        st.sidebar.markdown('''
        <hr/> <h6 style='text-align:center;color:grey;'>
        Tous droits réservés © 2023 <br/> TOUNDE - FOUPOUAPOUOGNIGNI - TAYAWELBA - KOTIEU 
        <br/> KEYCE - Master 1 - IA & BD <br/> Supervisé par M.ABDOURAMAN 
        <br/> Coordonateur Académique
        ''', unsafe_allow_html=True)

    if __name__=='__main__':
        main()

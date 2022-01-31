# Idée du projet

La première idée du projet était dans un premier temps de diviser le fichier `Base-Steering.py` en plusieurs sous fichier afin d'avoir une lecture plus simple, ainsi que de créer une class `Vecteur` et d'implémenter certaines fonctions (approximate distance). Les collisions ont été rajouté en considérant que toutes les voitures ont le même poids, cela peut se changer dans une prochaine version.

Par la suite, j'ai ajouté la "génération" des virages par Steering. Le problème avec la version initiale était que les voitures sortaient de la piste sur des angles importants. Pour ne pas développer d'algo complexe pour gérer ces virages, j'ai utilisé le trajet réel des voitures pour ajouter une courbe aux virages.

# Résultats

## Collisions

Pour les collisions, une application du théorème de thalès entre le vecteur entre les positions des deux véhicules et la distance souhaitée permet de faire en sorte que les voitures ne se rentrent pas dedans. _A noter que les collisions sont gérées une par une via une boucle, si une voiture est modifiée après rectification (par une autre collision), il peut y avoir un problème, mais globalement le rendu avec de nombreuses voitures reste satisfaisant._

![Collisions de nombreuses voitures](https://raw.githubusercontent.com/RomainBnfn/TPVoitureSteering/main/images/gif1.gif)

## Création de la route

Pour gérer la création des routes dans les virages, il est simplement nécessaire de détecter quand un véhicule sort de la route, puis d'enregistrer cette sortie dans le `track`. Si une sortie proche a déjà été enregistrée, pas besoin de la conserver (la route existe déjà), sinon il faut l'ajouter. Après quelques tours de voitures on observe une route avec des arrondis, de fait les voitures ne sortent plus du circuit.

![Collisions de nombreuses voitures](https://raw.githubusercontent.com/RomainBnfn/TPVoitureSteering/main/images/gif2.gif)

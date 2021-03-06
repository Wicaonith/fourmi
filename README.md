Le but de ce TP est d’avoir le chemin le plus court entre deux destinations à travers la ville de Nantes.


Pour cela nous avons en entrée les données de la ville de Nantes sous format .csv. La première étape du TP sera de transformer ce fichier CSV en un graphe que pourront parcourir des fourmis. Pour cela, nous avons des nœuds et des arêtes. A partir du moment où nous avons le graphe, il nous est possible de lâcher des fourmis dans la ville.


Une fourmi se présente sous la forme d’un dictionnaire de donnée avec en paramètre le nom, le poids par rapport à la distance parcouru, le point de départ, le point d’arrivé et un autre dictionnaire de données avec les rues déjà visitées et leurs index. Chaque fourmi est générée individuellement et fait son propre chemin. 


Le chemin à travers les rues de Nantes est géré aléatoirement. En effet lorsque les fourmis arrivent à un nœud (croisement de rue), alors elles choisissent aléatoirement la direction à prendre en vérifiant dans le dictionnaire des rues déjà visités qu’elles ne prennent pas deux fois le même chemin. Chaque rue visitée est ajouté dans le dictionnaire de données de la fourmi afin de ne pas parcourir deux fois le même chemin. Et pour optimiser ce chemin, il faut que les premières fourmis laissent une trace à leur suiveuse.


En effet chaque fourmi doit laisser une quantité de phéromones dans les rues visitées. Et quand une fourmi se retrouve à un nœud, elle privilégiera un chemin qui contient des phéromones. Et plus il y aura de phéromone dans les plus, plus les générations suivantes iront dans ces rues et finiront par avoir le chemin le plus court.


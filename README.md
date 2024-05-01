# Turtlebot circle drawing

Este repositório contém um script Python que controla um TurtleBot para desenhar um círculo no ROS.

## Pré-requisitos

Para rodar este projeto, você precisará ter o ROS 2, o `turtlesim` e o Python 3.8 ou superior instalados no seu sistema.

## Instruções de execução

Primeiramente rode no seu terminal o seguinte comando para clonar o repositório:

`git clone https://github.com/olin-med/PonderadaRosTurtlesim.git`

Em seguida, rode os dois comandos abaixo para buildar os pacotes e dar source no script de configuração do workspace:

`colcon buld`

`source install/local_setup.bash`

Agora abra uma nova janela no seu terminal.

Na primeira janela rode o seguinte comando:

`ros2 run draw_circle draw`

E, por fim, basta rodar na segunda janela:

`ros2 run turtlesim turtlesim_node`

Pronto! Uma janela deve abrir na qual a tartaruga spawnará e desenhará o círculo.

## Vídeo do projeto em execução:

[video](https://www.youtube.com/watch?v=ATgdTEat4w4)

Este código foi desenvolvido por Ólin Medeiros Costa.





# Prototipo-ViewSnakePDDL

<img alt="Header" width=100% src="https://capsule-render.vercel.app/api?type=waving&color=00ff00&height=100&section=header">

Esse foi um projeto que fiz na disciplina Fundamentos Lógicos em Inteligência Artificial. Basicamente, permite visualizar
os planos gerados pelo planejador PDDL para o domínio snake que participou da IPC 2018. Afinal, do que adianta um plano se não
podemos por para teste?

<h2>Para testar:</h2>

Caso queira testar basta baixar os arquivos e rodar o visualizador de acordo com o seguinte comando:

```python
python visualizador-snake-pddl.py [problem-name] [plan-name] [opt-interval]
```

Os nomes dos arquivos devem conter também a extensão. [opt-interval] se refere à velocidade da execução
da visualização, o padrão é 0.2, quanto menor mais rápido.

Lembrando que está ajustado para os planos gerados pelo planejador Madagascar. Caso outro seja utilizado é necessário ajustar o
código à sintaxe do planejador escolhido.

Requer a biblioteca pygame.

<h2>Visualização do plano de teste:</h2>

<p align="center"><img alt="Imagem do visualizador" width="75%" src="https://github.com/euyogi/Prototipo-ViewSnakePDDL/assets/46427886/13d866c6-b8e2-4ea7-8edb-8f957936bee4"></p>

<p align="center">
  Feito por: Yogi Nam de Souza Barbosa
</p>

<img alt="Footer" width=100% src="https://capsule-render.vercel.app/api?type=waving&color=00ff00&height=100&section=footer">

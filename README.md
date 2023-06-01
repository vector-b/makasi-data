## Objetivo do desafio

Construir uma API Restful em python que atinja o seguinte objetivo: dois metodos get onde será executado um processamento em cima de uma base de dados local localizada no diretório /src/datasets/ e retornará o resultado desse processamento.

## Como começar o desafio

Dar um fork no projeto, clonar o repositório em sua máquina local e criar um branch novo para o seu código.

## Histórias

• Ao utilizar o método get_list_of_constructions_form_ref eu preciso que seja retornado uma lista do campo "Ref" somente onde o campo "Report Forms Status" for "Closed" usando a dataset denominado "construction_data_forms.csv"

• Ao utilizar o método get_constructions_tasks_date_range eu preciso que seja retornado três valores referentes ao campo "Status Changed" do dataset denominado "construction_data_tasks.csv": a data mais antiga do conjunto, a data mais recente do conjunto e total de dias entre as duas datas, Exemplo: start_date: 01/01/2023; end_date: 31/01/2023; total_in_days: 30

• Você precisa disponibilziar a documentação básica da API para que possa ser utilizada por um terceiro que não conhece seu código.

• É necessário que a API possa ser testada através de um método interativo, como por exemplo, usando Swagger UI.

• Eu preciso ter um arquivo dockerfile para poder virtualizar a aplicação, gerando uma imagem dela para rodar com docker. Importante enviar as orientações de "docker run" para rodar o projeto.

## Referências

• Os datasets necessário para o teste se encontram no diretório /src/datasets/ dentro do projeto.

• Os datasets trazidos nesse projeto são abertos e originados do link: https://www.kaggle.com/datasets/claytonmiller/construction-and-project-management-example-data

## Observações

1. Utilize CORS aberto para qualquer origem de requisições.

2. Não é necessário criar metodos de autenticação, nesse momento você pode criar uma API de consulta pública e aberta.

## Requisitos Técnicos para a entrega do teste

• Sugerimos a utilização do FastAPI para criação da aplicação.

• Utilize seus padrões de organização de projeto, documentação e código.

• Pode ser utilizada qualquer lib adicional que julgar importante para o bom funcionamento da aplicação, mas não se esqueça de dar as orientações de instalação delas (caso seja necessário)

• A aplicação será rodada em localhost.

• Ainda na documentação, explicar a sua motivação de escolha das libs e frameworks (ou o motivo de ter feito na mão). Uma explicação sobre a estrutura do projeto também será bem vinda.

• É imprescindível que o teste desenvolvido funcione corretamente em qualquer máquina.


## Observações importantes

A ideia deste desafio é entender como você domina os conceitos de desenvolvimento de APIs, serviços, processamentos, virtualização e documentação. 

Não é pra ser um teste exaustivo. Objetivo é entregar a solução proposta de forma direta mas de forma replicavel, funcional e documentada para uso.

Além do que foi pedido nos requisitos técnicos acima, não existe “certo e errado”, da mesma forma que não vamos levar tudo ao pé da letra nos mínimos detalhes.

## Considerações finais

Buscamos entender seu perfil de desenvolvimento, resolução de problemas, raciocinio lógico e boas práticas de desenvolvimento. O papel desse profissional dentro do time é desenvolver serviços específicos da camada analítica e automação da empresa, dessa forma, buscamos profissionais criativos e orientados a solução.

Esperamos que você vá além do mínimo proposto e demostre o conhecimento que tem. O teste tem gaps propositais para você sugerir soluções, desenvolver ideias e provar na prática o porque a sua decisão pode ter um impacto positivo nessa tarefa.

No demais, o diálogo é sempre bem-vindo e incentivado, principalmente sugestões e discussões. Caso surjam dúvidas no processo, sintam-se à vontade para nos perguntar.

Boa sorte no teste!

Abraço!
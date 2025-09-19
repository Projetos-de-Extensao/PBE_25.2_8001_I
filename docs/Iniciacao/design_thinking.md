---
id: dt
title: Design Thinking
---

# Design Thinking

O Design Thinking (DT) é uma abordagem para a resolução de problemas, centrada no ser humano, que visa criar soluções inovadoras e impactantes, focando nas necessidades reais dos usuário.

---

## Capa



<span style="font-size:20px;">Projeto Back-end</span> 



<span style="font-size:20px;">Quinto Elemento</span>  


<span style="font-size:20px;">2025.2</span>  

<img src="https://i.pinimg.com/originals/36/80/48/3680488ab71368a1fea7a7fc2bbbd8f5.gif" alt="Descrição da imagem" width="150" />


---

##  Introdução

**Contexto do Projeto** 

A monitoria tem apresentado um crescimento significativo, com uma alta taxa de procura por parte dos alunos. No entanto, esse avanço não tem sido acompanhado por uma estrutura adequada. A ausência de um sistema próprio traz uma série de desafios que comprometem a eficiência, a organização e a confiabilidade do serviço, com tantos processos e informações sendo gerenciados de forma descentralizada, a operação acaba ficando vulnerável a erros e falhas de comunicação.

**Objetivo** 

Cria uma plataforma própria da monitoria:

- Permita que alunos se candidatem às vagas disponíveis
- Gerencia processos seletivos e as entrevistas, como aprova ou reprovar o aluno
- Visualização de horários e temas das monitorias
- Área de materiais de apoio e conteúdos extras
- Sistema de feedback e acompanhamento sobre as monitorias


**Público-Alvo**

Alunos, Monitores, Professores e Coordenadores


**Escopo** 

Desenvolver um site próprio para a monitoria, com o intuito de centralizar processos, melhorar a comunicação, reduzir erros operacionais e oferecer uma experiência mais eficiente e profissional aos alunos e monitores.

---

## Fases do Design Thinking

### Empatia

**Pesquisa**

- Realização de entrevistas com alunos que já participaram de programas de monitoria, visando compreender suas experiências, desafios e benefícios percebidos.
- Coleta de depoimentos de alunos que nunca participaram das monitorias, buscando identificar barreiras de acesso, falta de informação ou desinteresse.
- Entrevistas com professores e coordenadores para avaliar o impacto da monitoria no desempenho acadêmico dos alunos envolvidos e entender a perspectiva docente sobre o programa.

**Insights**

=== "Alta demanda exige estrutura"
    - A falta de estrutura pode comprometer a qualidade do serviço e a experiência dos alunos, como exemplo a comunicação depende de canais informais (grupos de WhatsApp, boca a boca).

    - A tendência é que a demanda continue crescendo. Um modelo manual não acompanha esse ritmo. Um sistema digital permite escalar com controle, mantendo a qualidade e ampliando o alcance da monitoria.

=== "Dados como ferramenta de melhoria"
    - Sem um sistema que registre e analise dados, perde-se a chance de entender padrões de engajamento, identificar dificuldades recorrentes e melhorar continuamente o serviço.

    - A ausência de um sistema também dificulta o acompanhamento do impacto da monitoria no desempenho acadêmico.

=== "Oportunidade de profissionalização"
    - A criação de um site próprio representa mais do que organização: é um passo rumo à profissionalização da monitoria. Uma plataforma bem estruturada transmite seriedade, facilita a gestão e abre espaço para inovação.



**Personas**

=== "Aluno"
    <span style="font-size:30px;">Lucas</span> 

    

    Idade: 19 anos

    Curso: Engenharia de Computação

    Perfil: Curioso, esforçado, mas com dificuldades em algumas disciplinas técnicas

    Objetivos: Melhorar o desempenho acadêmico, encontrar apoio acessível e confiável

    Frustrações: Falta de informações claras sobre monitorias, dificuldade em se inscrever, comunicação confusa

    Necessidades: Plataforma intuitiva, com horários visíveis, opção de feedback e acesso a materiais extras

=== "Monitor"
    <span style="font-size:30px;">João Victor</span> 

    

    Idade: 21 anos

    Curso: Engenharia Elétrica

    Perfil: Proativo, comunicativo, gosta de ensinar e tem facilidade com tecnologia

    Objetivos: Ser monitor da disciplina de Cálculo III para reforçar seu conhecimento, ajudar colegas e acumular experiência para o mestrado

    Frustrações: Conciliar a monitoria com os estudos e estágios, lidar com burocracia e falta de feedback estruturado


    Necessidades: Uma plataforma centralizada, com horários visíveis.
=== "Coordenador"
    <span style="font-size:30px;">Helena</span> 

    

    Idade: 38 anos

    Cargo: Coordenador de Monitoria Institucional

    Perfil: Estratégico, focado em resultados e escalabilidade

    Objetivos: Profissionalizar o programa, garantir eficiência e ampliar o alcance

    Frustrações: Falta de dados consolidados, dificuldade de comunicação entre setores, baixa adesão por desorganização

    Necessidades: Dashboard com métricas, relatórios automáticos, sistema centralizado e seguro
    

=== "Professor"
    <span style="font-size:30px;">Clayton</span> 

    

    Idade: 54 anos

    Área: Matemática Aplicada

    Perfil: Organizada, exigente, valoriza o impacto da monitoria no aprendizado

    Objetivos: Selecionar bons monitores, acompanhar o progresso dos alunos, reduzir carga administrativa

    Frustrações: Processos manuais, falta de histórico dos candidatos, dificuldade em manter controle

    Necessidades: Sistema de gestão de candidaturas, histórico de desempenho, comunicação direta com monitores


    

---


###  Definição

**Problema Central**

A tendência é que a demanda continue crescendo. Um modelo manual não acompanha esse ritmo, pois torna os processos mais lentos, sujeitos a falhas humanas e difíceis de padronizar. Essa limitação gera gargalos na execução das tarefas, compromete a qualidade dos resultados e aumenta a sobrecarga da equipe.

Além disso, a ausência de automação dificulta a escalabilidade do projeto, reduz a agilidade para responder às mudanças e prejudica a tomada de decisões estratégicas, já que muitas informações ficam dispersas ou desatualizadas.

Portanto, a manutenção de um fluxo manual coloca em risco a eficiência operacional e pode comprometer a sustentabilidade do projeto a longo prazo.

**Pontos de Vista** / *POV*

<div class="grid cards" markdown>

-  __Aluno:__ Quero encontrar uma monitoria que me ajude com aquela matéria difícil, mas é tudo tão desorganizado. Não sei onde ver os horários, quem são os monitores, nem como me inscrever. Se houvesse um site claro, com tudo centralizado, eu conseguiria participar mais e aproveitar melhor esse apoio
- __Monitor:__ Ser monitor agora é mais leve. Me sinto mais valorizado, mais organizado, e com mais tempo pra focar no que importa: ajudar meus colegas e crescer como futuro professor ou pesquisador.
-  __Professor:__ A monitoria é essencial para reforçar o aprendizado dos alunos, mas hoje tudo depende de planilhas e mensagens soltas. Eu preciso de uma plataforma que me permita acompanhar os candidatos, aprovar entrevistas e ver como os alunos estão evoluindo — sem perder tempo com burocracia
-  __Coordenador:__ A demanda por monitoria cresce a cada semestre, mas sem um sistema, fica impossível manter controle. Preciso de uma solução que centralize os dados, gere relatórios, facilite a comunicação entre todos os envolvidos e profissionalize o programa. A sustentabilidade do projeto depende disso.


</div>

###  Ideação

**Brainstorming**

A plataforma tem como objetivo principal digitalizar e integrar todas as etapas da monitoria acadêmica, desde a inscrição de alunos até o acompanhamento de desempenho pelos coordenadores. Ela será acessível via web e dispositivos móveis, com interfaces personalizadas para cada perfil de usuário.


**Seleção de Ideias**

...

**Ideias Selecionadas**

...

---

###  Prototipagem



**🎯 Visão Geral**

A plataforma será um sistema web responsivo, com acesso também por dispositivos móveis, voltado para centralizar e profissionalizar o programa de monitoria acadêmica. Ela atenderá às necessidades específicas de alunos, monitores, professores e coordenadores, oferecendo uma experiência intuitiva, organizada e eficiente.

=== " Interface do Aluno"

    - 📋 Visualização de vagas disponíveis por disciplina, horário e monitor responsável

    - 📝 Candidatura rápida com preenchimento de dados e justificativa

    - 📅 Agenda de monitorias com filtros por curso, matéria e dia da semana

    - 📚 Área de materiais de apoio e conteúdos extras organizados por disciplina

    - ⭐ Sistema de feedback pós-monitoria (avaliação do monitor, conteúdo e estrutura)

    - 🔔 Notificações sobre novas vagas, alterações de horário e lembretes de sessões

=== " Interface do Monitor"

    - 📌 Gerenciamento de horários e temas das monitorias

    - ✅ Aprovação ou reprovação de candidatos (com histórico e justificativa)

    - 📤 Upload de materiais de apoio e conteúdos extras

    - 📈 Acompanhamento dos feedbacks recebidos

    - 📊 Relatórios de presença e engajamento dos alunos

=== "  Interface do Professor/Coordenador"

    - 🧠 Visão estratégica do programa: número de monitorias, alunos atendidos, disciplinas com maior demanda

    - 📊 Relatórios automáticos com métricas de engajamento, desempenho e feedbacks

    - 🔍 Gestão dos processos seletivos: visualização de candidatos, entrevistas, aprovações

    - 📋 Visualização de candidatos à monitoria por disciplina

    - ✅ Aprovação de monitores com base em histórico acadêmico e entrevistas

    - 📂 Acesso a relatórios de desempenho e feedbacks dos alunos


**Materiais Utilizados**

![Figma](https://img.shields.io/badge/Figma-F24E1E?style=for-the-badge&logo=figma&logoColor=white)




###  Teste do Prototipo

...

**Feedback dos Usuários**

...

**Ajustes Realizados** 

...

**Resultados Finais** 

...

---

##  Conclusão

...



=== "Resultados Obtidos"
    ...

=== "Próximos Passos"
    ...

=== "Aprendizados"
    ...

---

## Anexos

---

## Autores

| Data       | Versão | Descrição            | Autor(es)                          |
|------------|--------|----------------------|------------------------------------|
| 04/09/2025 | 1.0    | Fiz o DT até o tópico "Fases do Design Thinkng". | Felipe Siaba |
| 18/09/2025 | 1.1    | Edição de alguns topicos e mais algumas partes | Felipe Siaba |





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

- Portal de Vagas: Interface para que coordenadores publiquem as vagas de monitoria, especificando a disciplina, os pré-requisitos, as responsabilidades e o número de vagas.
- Cadastro de Candidatos: Permite que os alunos interessados criem um perfil, anexem documentos relevantes (histórico escolar, currículo, carta de motivação) e se candidatem às vagas disponíveis.
- Seleção e Comunicação: Ferramentas para que os professores avaliem os candidatos, registrem suas avaliações e comuniquem o resultado (aprovação, lista de espera, reprovação) de forma padronizada.
- Geração de Relatórios Básicos: Emissão de listas de candidatos por vaga, monitores selecionados por disciplina e departamento.
- Registro de Frequência e Horas: Ferramenta para que o monitor registre suas horas trabalhadas e o professor supervisor as valide. Pode incluir a opção de registro por aplicativo móvel.
- Dashboard de Gestão: Painel de controle para o departamento com visão geral do número de monitores por curso, horas trabalhadas, status dos pagamentos e avaliações pendentes.
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

=== "Estrutura e Transparência para Escalar com Qualidade"
    A criação de um portal de vagas e um sistema de candidatura estruturado elimina a informalidade e democratiza o acesso à monitoria. Com critérios claros, documentos anexados e comunicação padronizada, o processo seletivo se torna mais justo, transparente e escalável — permitindo que a alta demanda seja atendida com organização e eficiência.

=== "Gestão Inteligente com Dados e Automação"
    Ferramentas como o registro de frequência, dashboards administrativos e geração de relatórios transformam a monitoria em um programa gerenciável e mensurável. Coordenadores e professores passam a tomar decisões com base em dados reais, reduzindo erros operacionais e fortalecendo a sustentabilidade do projeto a longo prazo.
    

=== "Valorização da Experiência de Alunos e Monitores"
    Ao integrar feedbacks, acompanhamento de desempenho e acesso a materiais de apoio, a plataforma promove uma experiência mais rica e profissional para todos os envolvidos. Monitores se sentem reconhecidos, alunos têm apoio acessível e os professores ganham agilidade - criando um ciclo virtuoso de aprendizado e colaboração.



**Personas**

=== "Aluno"
    <span style="font-size:30px;">Lucas</span> 

    

    Idade: 19 anos

    Curso: Engenharia de Computação

    Perfil: Curioso, esforçado, mas com dificuldades em algumas disciplinas técnicas

    Objetivos: Contribuir com colegas, reforçar seu próprio aprendizado e enriquecer o currículo para futuras oportunidades acadêmicas ou profissionais

    Frustrações: Dificuldade em encontrar os critérios de seleção e se candidatar às vagas disponíveis

    Necessidades: Portal de vagas com informações completas e atualizadas

=== "Monitor"
    <span style="font-size:30px;">João Victor</span> 

    

    Idade: 21 anos

    Curso: Engenharia Elétrica

    Perfil: Proativo, comunicativo, gosta de ensinar e tem facilidade com tecnologia

    Objetivos: Ser monitor da disciplina de Cálculo III para reforçar seu conhecimento, ajudar colegas e acumular experiência para o mestrado

    Frustrações: Dificuldade em conciliar monitoria com estudos e estágio, burocracia excessiva, falta de retorno sobre seu desempenho


    Necessidades: Uma plataforma centralizada registrar horas e frequência e feedbacks dos alunos e professores

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

O crescimento contínuo da demanda por monitorias nas instituições de ensino tem exposto a fragilidade de um modelo operacional manual, descentralizado e pouco padronizado. A ausência de uma plataforma própria compromete a transparência dos processos seletivos, dificulta a comunicação entre alunos, professores e coordenadores, e torna a gestão das atividades dos monitores ineficiente e suscetível a erros.

Sem um sistema digital integrado, tarefas como publicação de vagas, candidatura, avaliação, registro de horas e acompanhamento de desempenho são realizadas por meio de planilhas, e-mails e mensagens informais, gerando sobrecarga administrativa, baixa rastreabilidade e perda de dados importantes. Essa limitação impede a escalabilidade do programa, reduz a qualidade da experiência dos envolvidos e compromete a profissionalização da monitoria como ferramenta pedagógica.

**Pontos de Vista** / *POV*

<div class="grid cards" markdown>

-  __Aluno:__ Quero muito ser monitor da disciplina que eu domino, mas o processo é confuso demais. Não sei onde encontrar as vagas, quais são os critérios, nem como enviar meus documentos. Se houvesse uma plataforma clara, com tudo centralizado — desde a inscrição até o resultado
- __Monitor:__ Ser monitor agora é mais leve. Me sinto mais valorizado, mais organizado, e com mais tempo pra focar no que importa: ajudar meus colegas e crescer como futuro professor ou pesquisador.
-  __Professor:__ A monitoria é essencial para reforçar o aprendizado dos alunos, mas hoje tudo depende de planilhas e mensagens soltas. Eu preciso de uma plataforma que me permita acompanhar os candidatos, aprovar entrevistas e ver como os alunos estão evoluindo — sem perder tempo com burocracia
-  __Coordenador:__ A demanda por monitoria cresce a cada semestre, mas sem um sistema, fica impossível manter controle. Preciso de uma solução que centralize os dados, gere relatórios, facilite a comunicação entre todos os envolvidos e profissionalize o programa. A sustentabilidade do projeto depende disso.


</div>

###  Ideação

**Brainstorming**

...


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

    - ⭐ Sistema de feedback pós-monitoria (avaliação do monitor, conteúdo e estrutura)

    - 🔔 Notificações sobre novas vagas, alterações de horário e lembretes de sessões

=== " Interface do Monitor"

    - 📌 Gerenciamento de horários e temas das monitorias

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





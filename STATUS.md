💾 Save Point: OfertaHub (Fase 1 e 2 Concluídas)
📌 Resumo Executivo

O OfertaHub é um sistema automatizado de curadoria e disparo de ofertas. O núcleo duro (backend) e a integração com o primeiro canal de distribuição (Telegram) estão 100% operacionais e rodando de forma autônoma no sistema operacional (Fedora). O projeto encontra-se pausado aguardando a liberação de credenciais de APIs reais de afiliação (ex: Amazon).
🏗️ Arquitetura Atual (O que está pronto)

O sistema foi desenhado de forma modular no diretório BackEnd/AI/:

    O Cérebro (gerente_ia.py & config.py):

        Lógica de triagem rigorosa implementada com sucesso em Python.

        Avalia produtos com base no desconto real (%), nota mínima (ex: >4.0) e volume de avaliações (ex: >50).

        Gera um Score de Oferta (0-100) combinando esses três fatores com pesos específicos.

        Exporta as ofertas aprovadas para ofertas_aprovadas.json.

    O Simulador (mock_api.py):

        Fornece dados de teste imitando a estrutura de uma API real de e-commerce, permitindo que a automação rode e seja testada sem acesso externo aprovado.

    A Boca (disparador_telegram.py):

        Integração concluída com o bot do Telegram usando python-telegram-bot.

        Lê o JSON gerado pelo Cérebro e envia as mensagens para o canal.

        Utiliza formatação rica (ParseMode.MARKDOWN_V2) e botões inline ("🛒 Comprar na Amazon") para maximizar a conversão.

    A Orquestração e Automação (pipeline.py & systemd):

        Script pipeline.py une o Cérebro e a Boca em uma execução sequencial assíncrona.

        Automação nativa configurada no Linux via systemd user timers (ofertahub.service e ofertahub.timer).

        O sistema roda a cada 60 minutos em background constante (loginctl enable-linger), com logs isolados.

🛑 Onde Paramos exata e tecnicamente

A lógica de filtragem e a automação do sistema operacional estão perfeitas. O fluxo atual consome dados simulados de e-commerce. A transição para um modelo de produção real depende apenas da troca da fonte de dados.
🚀 Como Retomar (Próximos Passos para a IA e para o Lucas)

Quando você voltar ao projeto com acesso à API de afiliados, entregue este documento para a IA e solicite os seguintes passos:

    Fase 1.5 - Integração da API Real:

        Criar o arquivo amazon_api.py (ou shopee_api.py).

        Implementar a conexão com a API oficial utilizando as credenciais recém-adquiridas.

        Alterar o arquivo pipeline.py para importar a função de busca do novo arquivo real em vez do mock_api.py.

    Fase 3 - Interface Web (A Montra):

        Iniciar o desenvolvimento de um frontend leve (ex: Next.js / PWA).

        Fazer com que este site consuma o banco de dados (ou o mesmo JSON gerado) para mostrar as ofertas indexáveis no Google para quem não usa Telegram.

    Fase 4 - Expansão de Canais:

        Desenvolver o disparador_whatsapp.py usando a Cloud API para espelhar as postagens do Telegram.

💻 Cheat Sheet de Comandos (Fedora Linux)

Para você não ter que decorar os comandos de gerenciamento do robô que ficou rodando no seu notebook:

    Verificar se o robô vai rodar logo: systemctl --user list-timers ofertahub.timer

    Parar a automação temporariamente: systemctl --user stop ofertahub.timer

    Forçar o robô a rodar agora: systemctl --user start ofertahub.service

    Ver o histórico de ofertas (Logs): journalctl --user -u ofertahub -n 50
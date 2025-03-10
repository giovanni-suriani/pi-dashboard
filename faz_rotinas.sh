# Script para configurar a rotina
#!/bin/bash

# Arquivo de rotinas
this_path=$(pwd)
touch $this_path/run_pis_dashboard_tasks.sh
echo "caminho = $this_path"
echo "#!/bin/bash" > $this_path/run_pis_dashboard_tasks.sh
echo "# No inicio de cada mes, o script abaixo eh executado para:" >> $this_path/run_pis_dashboard_tasks.sh
echo "# 1. Deletar os graficos do mes passado" >> $this_path/run_pis_dashboard_tasks.sh
echo "# 2. Gerar os graficos mais requisitados do mes anterior" >> $this_path/run_pis_dashboard_tasks.sh
echo "# 3. Reinicar a contagem dos dados mais requisitados" >> $this_path/run_pis_dashboard_tasks.sh
echo "" >> $this_path/run_pis_dashboard_tasks.sh
echo "source $this_path/env/bin/activate" >> $this_path/run_pis_dashboard_tasks.sh
echo "python3 $this_path/src/manage.py clean_old_charts --delete_all" >> $this_path/run_pis_dashboard_tasks.sh
echo "python3 $this_path/src/manage.py make_common_charts --initial --delete_records" >> $this_path/run_pis_dashboard_tasks.sh
echo "o script foi criado com sucesso!"
echo "usaremos o crontab para configurar a rotina, a cada inicio de mes, o script sera executado as 3h da manha"
(crontab -l; echo "0 3 1 * * /bin/bash $this_path/run_pis_dashboard_tasks.sh >> $this_path/cron_output.log 2>&1" ) | crontab -

# chmod +x $this_path/run_pis_dashboard_tasks.sh
# echo "Rotina configurada com sucesso!"
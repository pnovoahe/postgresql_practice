# Database monitoring

El objetivo es configurar Exporter, Prometheus y Grafana de forma tal que podamos obtener gráficos y estadísticas de monitorización a la bases de datos "mydb" en Postgresql.

En este proyecto nos hemos apoyado en [Docker](https://www.docker.com/) para desplegar en forma de servicios independientes a las cuatro tecnologías: Exporter, Prometheus, Grafana, y Postgresql.

Una vez realizada la composición (ej. con `docker compose up`) accederíamos a Grafana para, manualmente, configurar su acceso a la fuente de datos de nuestro servidor Prometheus e importar un dashboard específico (ID [9628](https://grafana.com/grafana/dashboards/9628-postgresql-database/)) para las bases de datos de PostgreSQL.

El flujo de trabajo de esta solución es el siguiente:

1. **PostgreSQL &rArr; PostgreSQL Exporter**: 
    - *PostgreSQL Exporter* extrae métricas de *PostgreSQL*.

2. **PostgreSQL Exporter &rArr; Prometheus**: 

    - *PostgreSQL Exporter* proporciona las métricas para que *Prometheus* las almacene y gestione.

3. **Prometheus &rArr; Grafana**: 

    - *Grafana* visualiza las métricas que le brinda *Prometheus* a través de dashboards configurables, incluyendo gráficos y una interfaz amigable.


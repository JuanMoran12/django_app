document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('form-busqueda');
    const resultadosDiv = document.querySelector('.resultados-busqueda');

    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            buscarInformes();
        });
    }

    function buscarInformes() {
        const formData = new FormData(searchForm);
        const searchParams = new URLSearchParams();
        
        for (const [key, value] of formData.entries()) {
            if (value) {
                searchParams.append(key, value);
            }
        }

        resultadosDiv.innerHTML = '<div class="loading">Buscando informes...</div>';

        fetch(`/mostrar_informe/?${searchParams.toString()}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error en la respuesta del servidor');
                }
                return response.json();
            })
            .then(data => {
                mostrarResultados(data.porcentajes);
            })
            .catch(error => {
                console.error('Error:', error);
                resultadosDiv.innerHTML = `
                    <div class="error">
                        <i class="fas fa-exclamation-circle"></i>
                        Error al cargar los datos. Por favor, intente nuevamente.
                    </div>`;
            });
    }

    function mostrarResultados(porcentajes) {
        resultadosDiv.innerHTML = '';

        if (!porcentajes || porcentajes.length === 0) {
            const noResults = document.createElement('div');
            noResults.className = 'no-results';
            noResults.innerHTML = `
                <i class="fas fa-search"></i>
                No se encontraron resultados para la búsqueda.
            `;
            resultadosDiv.appendChild(noResults);
            return;
        }

        const listaResultados = document.createElement('div');
        listaResultados.className = 'lista-resultados';

        porcentajes.forEach(item => {
            // Determine status class based on approval percentage
            let statusClass = 'bajo';
            if (item.indice_aprobacion >= 80) {
                statusClass = 'alto';
            } else if (item.indice_aprobacion >= 50) {
                statusClass = 'medio';
            }

            // Create elements securely
            const itemResultado = document.createElement('div');
            itemResultado.className = 'item-resultado';

            const icon = document.createElement('i');
            icon.className = 'fas fa-file-alt';

            const contenido = document.createElement('div');
            contenido.className = 'resultado-contenido';

            const h4 = document.createElement('h4');
            h4.textContent = item.carrera || 'Sin nombre';

            const fechaSpan = document.createElement('span');
            fechaSpan.className = 'resultado-fecha';
            fechaSpan.innerHTML = `<i class="far fa-calendar-alt"></i> ${new Date(item.fecha).toLocaleString()}`;

            const porcentajeDiv = document.createElement('div');
            porcentajeDiv.className = 'resultado-porcentaje';
            const barraProgreso = document.createElement('div');
            barraProgreso.className = `barra-progreso ${statusClass}`;
            barraProgreso.style.width = `${item.indice_aprobacion}%`;
            barraProgreso.textContent = `${item.indice_aprobacion}%`;
            porcentajeDiv.appendChild(barraProgreso);

            const datosDiv = document.createElement('div');
            datosDiv.className = 'resultado-datos';
            datosDiv.innerHTML = `
                <span><i class="fas fa-desktop"></i> ${item.equipos_evaluados} equipos</span>
                <span><i class="fas fa-check"></i> ${item.equipos_aprobados} aprobados</span>
                <span><i class="fas fa-times"></i> ${item.equipos_reprobados} reprobados</span>
            `;

            contenido.appendChild(h4);
            contenido.appendChild(fechaSpan);
            contenido.appendChild(porcentajeDiv);
            contenido.appendChild(datosDiv);

            itemResultado.appendChild(icon);
            itemResultado.appendChild(contenido);

            listaResultados.appendChild(itemResultado);
        });

        resultadosDiv.appendChild(listaResultados);
    }
});

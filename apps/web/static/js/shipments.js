// Selectores DOM
const printerSelector = document.getElementById('printerSelector');
const configElement = document.getElementById('configModal');
const configModal = new bootstrap.Modal(configElement);
const addElement = document.getElementById('addModal');
const addModal = new bootstrap.Modal(addElement);
const configButton = document.getElementById('configButton');
const packageAmountSelect = document.getElementById('packageAmountSelect');
const shipmentForm = document.getElementById('shipmentForm');
const addForm = document.getElementById('addForm');
const addButton = document.getElementById('addButton');

// Variables globales
let isModalOpening = false;

// Funciones de utilidad
const shipmentsData = async () => {
    try {
        const response = await fetch('/api/v1/shipments/');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching shipments:', error);
        throw error;
    }
};

function formatShipmentDetails(d) {
    return `
        <div class="d-flex justify-content-around align-items-center gap-2">
            <div class="d-flex flex-column text-center">
                <p class="mb-1"><strong>Fecha de envío:</strong> ${d.creation_date.split('T')[0]} ${d.creation_date.split('T')[1].substring(0, 5)}</p>
                <p class="mb-1"><strong>Estado:</strong> ${d.status.description}</p>
                <p class="mb-1"><strong>Ultima actualización</strong> ${d.update_date.split('T')[0]} ${d.update_date.split('T')[1].substring(0, 5)}</p>
            </div>
            <div class="d-flex flex-column text-center">
                <p class="mb-1"><strong>Fecha de entrega:</strong> ${d.delivery_date}</p>
                <p class="mb-1"><strong>Dirección de entrega:</strong> ${d.delivery_address}</p>
                <p class="mb-1"><strong>Tracking Number:</strong> ${d.tracking_number}</p>
            </div>
        </div>
    `;
}

async function printQR(tracking_number, qr_code, sender, recipient) {
    const cargaUtil = {
        "serial": "",
        "nombreImpresora": getCookie('printer'),
        "operaciones": [
            {
                "nombre": "Iniciar",
                "argumentos": []
            },
            {
                "nombre": "EstablecerAlineacion",
                "argumentos": [
                    1
                ]
            },
            {
                "nombre": "EscribirTexto",
                "argumentos": [
                    "\n\n\n"
                ]
            },
            {
                "nombre": "EstablecerTamañoFuente",
                "argumentos": [
                    3,
                    3
                ]
            },
            {
                "nombre": "EscribirTexto",
                "argumentos": [
                    tracking_number + "\n"
                ]
            },
            {
                "nombre": "EscribirTexto",
                "argumentos": [
                    "\n\n\n"
                ]
            },
            {
                "nombre": "EstablecerAlineacion",
                "argumentos": [
                  0
                ]
            },
            {
                "nombre": "EscribirTexto",
                "argumentos": [
                    "Remitente: " + sender + "\n"      
                ]
            },
            {
                "nombre": "EscribirTexto",
                "argumentos": [
                  "\n\n"
                ]
            },
            {
                "nombre": "EscribirTexto",
                "argumentos": [
                    "Destinatario: " + recipient + "\n"      
                ]
            },
            {
                "nombre": "EscribirTexto",
                "argumentos": [
                  "\n\n\n"
                ]
            },
            {
                "nombre": "DescargarImagenDeInternetEImprimir",
                "argumentos": [
                    qr_code,
                    500,
                    0,
                    false
                ]
            },
            {
                "nombre": "EscribirTexto",
                "argumentos": [
                    "\n\n\n\n\n"
                ]
            },
            {
                "nombre": "Corte",
                "argumentos": [
                  8
                ]
            }
        ]
    };

    try {
        const respuestaHttp = await fetch("http://localhost:2811/imprimir", { 
            method: "POST", 
            body: JSON.stringify(cargaUtil),
            headers: {
                'Content-Type': 'application/json'
            }
        }); 

        const respuesta = await respuestaHttp.json(); 
        
        if (respuesta.ok) { 
            console.log("Impreso correctamente");
            return true;
        } else { 
            console.error("Petición ok pero error en el plugin: " + respuesta.message); 
            return false;
        } 
    } catch (error) {
        console.error("Error al imprimir:", error);
        return false;
    }
}

// Configuración de DataTable
async function initializeDataTable() {
    const shipments = await shipmentsData();
    
    const table = new DataTable('#shipmentsTable', {
        data: shipments,
        paging: false,
        ordering: false,
        responsive: true,
        info: false,
        scrollY: '65vh',
        scrollCollapse: true,
        columns: [
            {
                className: 'dt-control text-center align-middle',
                defaultContent: '<i class="ti ti-text-plus fs-4 me-0"></i>',
                responsivePriority: 1
            },
            { data: 'tracking_number', responsivePriority: 2 },
            { data: 'sender', responsivePriority: 4 },
            { data: 'recipient', responsivePriority: 2 },
        ],
        language: {
            url: 'https://cdn.datatables.net/plug-ins/2.3.0/i18n/es-ES.json',
        },
        columnDefs: [
            {
                targets: '_all',
                className: 'text-center align-middle'
            }
        ],
    });

    return table;
}

// Manejadores de eventos
async function handlePrinterSelection(event) {
    if (event.ctrlKey && (event.key === 'i' || event.key === 'I')) {
        event.preventDefault();
        
        if (isModalOpening) return;
        isModalOpening = true;

        printerSelector.innerHTML = '';

        try {
            const respuestaHttp = await fetch("http://localhost:2811/impresoras");
            const listaDeImpresoras = await respuestaHttp.json();

            listaDeImpresoras.forEach(nombreImpresora => {
                const option = document.createElement('option');
                option.value = nombreImpresora;
                option.textContent = nombreImpresora;
                printerSelector.appendChild(option);
            });
        } catch (error) {
            console.error('Error al cargar impresoras:', error);
            const option = document.createElement('option');
            option.textContent = 'Error al cargar impresoras';
            printerSelector.appendChild(option);
        }

        configModal.show();
        isModalOpening = false;
    }
}

async function handleAddButtonClick() {
    packageAmountSelect.innerHTML = '';

    try {
        const response = await fetch('/api/v1/packages/');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const packages = await response.json();
        
        packages.forEach(pkg => {
            const option = document.createElement('option');
            option.value = pkg.id;
            option.textContent = `${pkg.name} - ${pkg.mount}`;
            packageAmountSelect.appendChild(option);
        });
        packageAmountSelect.selectedIndex = -1;
    } catch (error) {
        console.error('Error al cargar paquetes:', error);
        const option = document.createElement('option');
        option.textContent = 'Error al cargar paquetes';
        packageAmountSelect.appendChild(option);
    }

    addModal.show();
}

async function handleAddFormClick() {
    const formData = new FormData(shipmentForm);
    
    formData.append('package_amount', packageAmountSelect.value);
    
    try {
        const response = await fetch('/api/v1/shipments/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }
        const data = await response.json();

        printQR(data.tracking_number, data.qr_code, data.sender, data.recipient);
        addModal.hide();
        location.reload();
    } catch (error) {
        console.error('Error:', error);
    }
}

// Función auxiliar para obtener el token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Event Listeners
document.addEventListener('DOMContentLoaded', async () => {
    const table = await initializeDataTable();
    
    table.on('click', 'td.dt-control', function (e) {
        let tr = e.target.closest('tr');
        let row = table.row(tr);
    
        if (row.child.isShown()) {
            row.child.hide();
        } else {
            row.child(formatShipmentDetails(row.data())).show();
        }
    });
});

document.addEventListener('keydown', handlePrinterSelection);

configElement.addEventListener('hidden.bs.modal', () => {
    console.log('Cerrando modal');
    printerSelector.innerHTML = '';
});

addElement.addEventListener('hidden.bs.modal', () => {
    shipmentForm.reset();
    packageAmountSelect.innerHTML = '';
});

configButton.addEventListener('click', () => {
    const selectedPrinter = printerSelector.value;
    if (selectedPrinter) {
        document.cookie = `printer=${selectedPrinter}; max-age=${10*365*24*60*60}; path=/`;
        console.log('Impresora guardada:', selectedPrinter);
        configModal.hide();
    }
});

addButton.addEventListener('click', handleAddButtonClick);
addForm.addEventListener('click', handleAddFormClick);
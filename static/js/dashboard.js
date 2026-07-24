// ==========================================
// Smart Meters Company Limited
// Dashboard Charts
// ==========================================

// Complaint Trend Chart

const trendCanvas = document.getElementById("trendChart");

if (trendCanvas) {

    new Chart(trendCanvas, {

        type: "line",

        data: {

            labels: [

                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun"

            ],

            datasets: [{

                label: "Complaints",

                data: [

                    5,
                    9,
                    7,
                    12,
                    8,
                    14

                ],

                fill: true,

                tension: .4,

                borderWidth: 3

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false

        }

    });

}


// Complaint Category Chart

const pieCanvas = document.getElementById("pieChart");

if (pieCanvas) {

    new Chart(pieCanvas, {

        type: "doughnut",

        data: {

            labels: [

                "Billing",
                "Meter Fault",
                "Installation",
                "Power Supply"

            ],

            datasets: [{

                data: [

                    18,
                    12,
                    8,
                    5

                ]

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false

        }

    });

}
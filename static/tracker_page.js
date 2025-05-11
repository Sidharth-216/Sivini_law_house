document.addEventListener("DOMContentLoaded", function() {
    // Data for the charts
    const caseStatusData = {
        labels: ['Pending', 'Ongoing', 'Closed'],
        datasets: [{
            data: [45, 35, 20], // Sample data
            backgroundColor: ['#f39c12', '#3498db', '#2ecc71'],
            hoverBackgroundColor: ['#e67e22', '#2980b9', '#27ae60'],
        }]
    };

    const casesByLawyerData = {
        labels: ['Lawyer 1', 'Lawyer 2', 'Lawyer 3'],
        datasets: [{
            label: 'Number of Cases',
            data: [10, 5, 8], // Sample data
            backgroundColor: '#3498db',
            borderColor: '#2980b9',
            borderWidth: 1
        }]
    };

    const overallProgressData = {
        labels: ['Completed', 'In Progress'],
        datasets: [{
            data: [60, 40], // Sample data
            backgroundColor: ['#27ae60', '#f39c12'],
        }]
    };

    // Case Status Pie Chart
    const ctx1 = document.getElementById('caseStatusChart').getContext('2d');
    new Chart(ctx1, {
        type: 'pie',
        data: caseStatusData,
    });

    // Cases by Lawyer Bar Chart
    const ctx2 = document.getElementById('casesByLawyerChart').getContext('2d');
    new Chart(ctx2, {
        type: 'bar',
        data: casesByLawyerData,
        options: {
            responsive: true,
            scales: {
                x: {
                    beginAtZero: true
                }
            }
        }
    });

    // Overall Progress Doughnut Chart
    const ctx3 = document.getElementById('overallProgressChart').getContext('2d');
    new Chart(ctx3, {
        type: 'doughnut',
        data: overallProgressData,
    });
});

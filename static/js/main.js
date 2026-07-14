// Main Frontend Scripts for Fake Profile Detection System

document.addEventListener('DOMContentLoaded', function() {
    
    // --- 1. HANDLE PROFILE PREDICTION VIA AJAX ---
    const predictForm = document.getElementById('predictForm');
    if (predictForm) {
        predictForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const submitBtn = predictForm.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.innerHTML;
            
            // Show loading state
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Analyzing Profile...';
            
            const formData = new FormData(predictForm);
            
            fetch('/predict', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;
                
                if (data.success) {
                    const resultBox = document.getElementById('resultBox');
                    const resultBadge = document.getElementById('resultBadge');
                    const resultConfidence = document.getElementById('resultConfidence');
                    const resultBar = document.getElementById('resultBar');
                    const resultReason = document.getElementById('resultReason');
                    
                    // Reset classes
                    resultBox.style.display = 'block';
                    resultBox.className = 'result-box';
                    
                    if (data.prediction === 'Fake') {
                        resultBox.classList.add('fake');
                        resultBadge.className = 'badge-fake mb-3';
                        resultBadge.innerText = 'FAKE PROFILE';
                    } else {
                        resultBox.classList.add('genuine');
                        resultBadge.className = 'badge-genuine mb-3';
                        resultBadge.innerText = 'GENUINE PROFILE';
                    }
                    
                    resultConfidence.innerText = data.confidence;
                    resultReason.innerText = data.reason;
                    
                    // Trigger confidence bar animation
                    setTimeout(() => {
                        resultBar.style.width = (data.probability * 100) + '%';
                    }, 100);
                    
                    // Scroll to result
                    resultBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                    
                    // Optional: Refresh history list if it exists on page
                    appendPredictionToHistoryTable(data, formData.get('username'));
                } else {
                    alert('Error: ' + data.error);
                }
            })
            .catch(error => {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;
                console.error('Error running prediction:', error);
                alert('An error occurred during prediction. Please try again.');
            });
        });
    }

    // Helper to dynamically insert prediction into dashboard history table
    function appendPredictionToHistoryTable(data, username) {
        const tableBody = document.getElementById('historyTableBody');
        if (!tableBody) return;
        
        // Remove empty state row if present
        const emptyRow = tableBody.querySelector('.empty-row');
        if (emptyRow) {
            emptyRow.remove();
        }
        
        const now = new Date();
        const dateString = now.toISOString().slice(0, 19).replace('T', ' ');
        
        const newRow = document.createElement('tr');
        const badgeClass = data.prediction === 'Fake' ? 'badge-fake' : 'badge-genuine';
        
        newRow.innerHTML = `
            <td><strong>@${username}</strong></td>
            <td><span class="${badgeClass}">${data.prediction.toUpperCase()}</span></td>
            <td>${data.confidence}</td>
            <td><small class="text-secondary">${data.reason}</small></td>
            <td>${dateString}</td>
        `;
        
        // Insert at beginning of table
        tableBody.insertBefore(newRow, tableBody.firstChild);
    }
    
    // --- 2. SEARCH & FILTER PREDICTIONS TABLE ---
    const searchInput = document.getElementById('searchPredictInput');
    const filterSelect = document.getElementById('filterPredictSelect');
    
    if (searchInput || filterSelect) {
        const triggerFilter = function() {
            const query = searchInput ? searchInput.value.toLowerCase().trim() : '';
            const statusFilter = filterSelect ? filterSelect.value : 'all';
            
            const rows = document.querySelectorAll('#historyTableBody tr:not(.empty-row)');
            
            rows.forEach(row => {
                const usernameCell = row.cells[0].textContent.toLowerCase();
                const statusCell = row.cells[1].textContent.trim(); // "FAKE" or "GENUINE"
                
                let matchesSearch = usernameCell.includes(query);
                let matchesStatus = (statusFilter === 'all') || 
                                    (statusFilter === 'fake' && statusCell === 'FAKE') || 
                                    (statusFilter === 'genuine' && statusCell === 'GENUINE');
                                    
                if (matchesSearch && matchesStatus) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        };
        
        if (searchInput) searchInput.addEventListener('keyup', triggerFilter);
        if (filterSelect) filterSelect.addEventListener('change', triggerFilter);
    }

    // --- 3. CHARTJS INTEGRATION (ADMIN DASHBOARD ONLY) ---
    const adminAnalytics = document.getElementById('adminAnalyticsMarker');
    if (adminAnalytics) {
        fetch('/api/admin/analytics')
        .then(response => response.json())
        .then(analyticsData => {
            renderPieChart(analyticsData.pie_data);
            renderLineChart(analyticsData.line_data);
            renderBarChart(analyticsData.bar_data);
        })
        .catch(error => console.error('Error fetching analytics:', error));
    }
    
    function renderPieChart(pieData) {
        const ctx = document.getElementById('pieChart');
        if (!ctx) return;
        
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: pieData.labels,
                datasets: [{
                    data: pieData.data,
                    backgroundColor: ['#ef4444', '#10b981'],
                    borderColor: '#111827',
                    borderWidth: 2,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#9ca3af',
                            font: { family: 'Plus Jakarta Sans', size: 12 }
                        }
                    }
                }
            }
        });
    }
    
    function renderLineChart(lineData) {
        const ctx = document.getElementById('lineChart');
        if (!ctx) return;
        
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: lineData.labels,
                datasets: [
                    {
                        label: 'Fake Profiles Detected',
                        data: lineData.fake,
                        borderColor: '#ef4444',
                        backgroundColor: 'rgba(239, 68, 68, 0.1)',
                        fill: true,
                        tension: 0.4,
                        borderWidth: 2
                    },
                    {
                        label: 'Genuine Profiles Detected',
                        data: lineData.genuine,
                        borderColor: '#10b981',
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        fill: true,
                        tension: 0.4,
                        borderWidth: 2
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: { color: '#9ca3af', font: { family: 'Plus Jakarta Sans' } }
                    }
                },
                scales: {
                    x: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#9ca3af' }
                    },
                    y: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#9ca3af', stepSize: 1 }
                    }
                }
            }
        });
    }
    
    function renderBarChart(barData) {
        const ctx = document.getElementById('barChart');
        if (!ctx) return;
        
        // Clean feature labels for display (e.g. replace underscores)
        const labels = barData.features.map(f => f.replace(/_/g, ' ').toUpperCase());
        
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Feature Importance Score',
                    data: barData.importances,
                    backgroundColor: 'rgba(99, 102, 241, 0.75)',
                    hoverBackgroundColor: '#6366f1',
                    borderColor: '#6366f1',
                    borderWidth: 1,
                    borderRadius: 5
                }]
            },
            options: {
                indexAxis: 'y', // Horizontal bar chart
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#9ca3af' }
                    },
                    y: {
                        grid: { display: false },
                        ticks: { color: '#9ca3af', font: { size: 10 } }
                    }
                }
            }
        });
    }
});

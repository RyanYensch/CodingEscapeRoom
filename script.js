window.addEventListener('DOMContentLoaded', () => {
    const params       = new URLSearchParams(window.location.search);
    const timeTakenSec = parseFloat(params.get('time')) || 0;
    const testsRun     = parseInt(params.get('testsRun')) || 0;
    const testsFailed  = parseInt(params.get('testsFailed')) || 0;
    const compFails    = parseInt(params.get('compilesFailed')) || 0;
  
    const bestKey = 'bestTimeSec';
    let bestSec = parseFloat(localStorage.getItem(bestKey));
    if (!bestSec || timeTakenSec < bestSec) {
      bestSec = timeTakenSec;
      localStorage.setItem(bestKey, bestSec);
    }
  
    function formatMMSS(sec) {
      const m = Math.floor(sec / 60);
      const s = Math.floor(sec % 60);
      return `${m}:${s.toString().padStart(2,'0')}`;
    }
  
    document.getElementById('timeTaken').textContent    = `Time Taken: ${formatMMSS(timeTakenSec)}`;
    document.getElementById('bestTime').textContent     = `Best Time: ${formatMMSS(bestSec)}`;
    document.getElementById('testsRun').textContent     = `Total Tests Run: ${testsRun}`;
    document.getElementById('testsFailed').textContent  = `Total Tests Failed: ${testsFailed}`;
    document.getElementById('compilesFailed').textContent = `Total Compilation Fails: ${compFails}`;
  
    const ctx = document.getElementById('timeChart').getContext('2d');
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['current', 'best'],
        datasets: [{
          label: 'time (mm:ss)',
          data: [timeTakenSec, bestSec],
          backgroundColor: ['rgba(54,162,235,0.6)', 'rgba(255,99,132,0.6)'],
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: value => formatMMSS(value)
            }
          }
        },
        plugins: {
          title: {
            display: true,
            text: 'Time Comparison'
          }
        }
      }
    });
  });
  
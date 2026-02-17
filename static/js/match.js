document.addEventListener('DOMContentLoaded', function() {
    const matchForm = document.getElementById('matchForm');
    const successMessage = document.getElementById('successMessage');
    
    matchForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const group = document.getElementById('group').value;
        const matchData = [];
        
        // Get all rank entries
        const teamInputs = document.querySelectorAll('.team-input');
        const killsInputs = document.querySelectorAll('.kills-input');
        
        // Validate and collect data
        const teamNames = new Set();
        let isValid = true;
        
        for (let i = 0; i < teamInputs.length; i++) {
            const teamName = teamInputs[i].value.trim();
            const kills = parseInt(killsInputs[i].value);
            
            if (!teamName) {
                alert(`Please enter team name for Rank ${i + 1}`);
                isValid = false;
                break;
            }
            
            if (teamNames.has(teamName)) {
                alert(`Duplicate team name: ${teamName}. Each team can only appear once.`);
                isValid = false;
                break;
            }
            
            teamNames.add(teamName);
            
            matchData.push({
                rank: i + 1,
                team: teamName,
                kills: kills
            });
        }
        
        if (!isValid) return;
        
        // Confirm submission
        if (!confirm(`Save match data for Group ${group}?`)) {
            return;
        }
        
        // Disable submit button
        const submitBtn = matchForm.querySelector('.submit-btn');
        const originalText = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = '⏳ Saving...';
        
        try {
            // Send data to server
            const response = await fetch('/api/save-match', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    group: group,
                    match_data: matchData
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Show success message
                successMessage.style.display = 'block';
                successMessage.innerHTML = `<p>✓ ${result.message}</p>`;
                
                // Reset form
                matchForm.reset();
                
                // Scroll to top
                window.scrollTo({ top: 0, behavior: 'smooth' });
                
                // Redirect after 2 seconds
                setTimeout(() => {
                    window.location.href = `/leaderboard/${group}`;
                }, 2000);
            } else {
                alert(`Error: ${result.message}`);
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }
        } catch (error) {
            alert('Error saving match data. Please try again.');
            console.error('Error:', error);
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    });
    
    // Auto-focus first team input
    const teamInputs = document.querySelectorAll('.team-input');
    if (teamInputs.length > 0) {
        teamInputs[0].focus();
    }
    
    // Add Enter key navigation
    const allInputs = document.querySelectorAll('.team-input, .kills-input');
    allInputs.forEach((input, index) => {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                const nextIndex = index + 1;
                if (nextIndex < allInputs.length) {
                    allInputs[nextIndex].focus();
                } else {
                    // Submit form if last input
                    matchForm.querySelector('.submit-btn').focus();
                }
            }
        });
    });
});

document.getElementById('mortgage-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const principal = parseFloat(document.getElementById('principal').value);
    const annualRate = parseFloat(document.getElementById('epr').value);
    const termYears = parseInt(document.getElementById('term').value);
    const paymentsMade = parseInt(document.getElementById('paid').value);

    if (isNaN(principal) || isNaN(annualRate) || isNaN(termYears) || isNaN(paymentsMade) || principal < 0 || annualRate < 0 || termYears < 0 || paymentsMade < 0) {
        alert("Please enter valid, non-negative numbers in all fields.");
        return;
    }

    const { monthlyPayment, outstandingBalance } = calculateOutstandingBalance(principal, annualRate, termYears, paymentsMade);

    const resultsContainer = document.getElementById('results');
    if (outstandingBalance > 0) {
        const principalPaidOff = principal - outstandingBalance;

        document.getElementById('monthly-payment').textContent = `$${monthlyPayment.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
        document.getElementById('outstanding-balance').textContent = `$${outstandingBalance.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
        document.getElementById('principal-paid').textContent = `$${principalPaidOff.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
        
        resultsContainer.style.display = 'block';
    } else {
        resultsContainer.innerHTML = '<h3 class="results-title">Loan Paid Off</h3><p>Based on your input, this loan appears to be fully paid off.</p>';
        resultsContainer.style.display = 'block';
    }
});

function calculateOutstandingBalance(principal, annualRate, termYears, paymentsMade) {
    if (principal <= 0) {
        return { monthlyPayment: 0, outstandingBalance: 0 };
    }

    const monthlyRate = (annualRate / 100) / 12;
    const totalPayments = termYears * 12;

    if (paymentsMade >= totalPayments) {
        return { monthlyPayment: 0, outstandingBalance: 0 }; // Loan is fully paid
    }

    let monthlyPayment;
    if (monthlyRate > 0) {
        const numeratorM = monthlyRate * Math.pow(1 + monthlyRate, totalPayments);
        const denominatorM = Math.pow(1 + monthlyRate, totalPayments) - 1;
        monthlyPayment = principal * (numeratorM / denominatorM);
    } else { // Handle zero interest case
        monthlyPayment = principal / totalPayments;
    }

    let balance;
    if (monthlyRate > 0) {
        const numeratorB = Math.pow(1 + monthlyRate, totalPayments) - Math.pow(1 + monthlyRate, paymentsMade);
        const denominatorB = Math.pow(1 + monthlyRate, totalPayments) - 1;
        balance = principal * (numeratorB / denominatorB);
    } else { // Handle zero interest case
        balance = principal - (monthlyPayment * paymentsMade);
    }

    return { monthlyPayment, outstandingBalance: balance };
}

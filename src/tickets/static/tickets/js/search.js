function searchTicket() {
// This function searches through each ticket name for user search input.
// It hides the ticket name if user input is not inside ticket name.

    let search = document.getElementById('ticket-search').value.toUpperCase();
    let ticketsTable = document.getElementById('tickets-table');
    let tickets = ticketsTable.getElementsByTagName('tr');

    for (let i = 0; i < tickets.length; ++i) {
        let ticketName = tickets[i].getElementsByTagName('td')[0];

        if (ticketName) {
            let text = ticketName.textContent || ticketName.innerText;

            if (text.toUpperCase().indexOf(search) > -1)
                tickets[i].style.display = '';
            else
                tickets[i].style.display = 'none';
        }
    }
}

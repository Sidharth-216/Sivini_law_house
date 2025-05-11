document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        events: [
            // Example events
            {
                title: 'Business Meeting',
                start: '2024-11-10T10:00:00',
                end: '2024-11-10T12:00:00'
            },
            {
                title: 'Client Consultation',
                start: '2024-11-12T14:00:00',
                end: '2024-11-12T15:00:00'
            },
            {
                title: 'Court Hearing',
                start: '2024-11-15T09:00:00',
                end: '2024-11-15T11:00:00'
            }
        ],
        editable: true,
        selectable: true,
        eventClick: function(info) {
            alert('Event: ' + info.event.title);
        },
        select: function(info) {
            var title = prompt('Event Title:');
            if (title) {
                calendar.addEvent({
                    title: title,
                    start: info.start,
                    end: info.end,
                    allDay: info.allDay
                });
            }
            calendar.unselect();
        }
    });

    calendar.render();
});

document.addEventListener('DOMContentLoaded', () => {
    // Popup warning message
    document.querySelectorAll('button.remove-button').forEach((button) => {
        button.onclick = () => {
            // Disable all other buttons
            document.querySelectorAll('button').forEach((btn) => {
                btn.disabled = true
            })

            // Get template
            const template = document.querySelector('template#removal-warning-template')

            // Add template to page
            const body = document.querySelector('body')
            body.appendChild(template.content.cloneNode(true))

            // Set background of page to be darker
            body.style.backgroundColor = 'rgba(0, 0, 0, 0.2)'

            // Set onclick for new buttons
            document.querySelector('div#removal-warning button.yes').onclick = () => {
                // Get csrf_token from cookies
                const token = document.cookie.match(new RegExp(`(^| )csrftoken=([^;]+)`))[2]

                console.log(button)
                console.log(button.dataset)
                console.log(button.dataset.id)

                fetch('/account/remove', {
                    method: 'POST',
                    body: JSON.stringify({
                        'id': button.dataset.id
                    }),
                    headers: {
                        'X-CSRFToken': token,
                    },
                })

                // Set background color back
                body.style.backgroundColor = '#fff'

                // Enable all other buttons
                document.querySelectorAll('button').forEach((button) => {
                    button.disabled = false
                })

                // Delete popup
                document.querySelector('div#removal-warning').remove()
            }
            document.querySelector('div#removal-warning button.no').onclick = () => {
                // Set background color back
                body.style.backgroundColor = '#fff'

                // Enable all other buttons
                document.querySelectorAll('button').forEach((button) => {
                    button.disabled = false
                })

                // Delete popup
                document.querySelector('div#removal-warning').remove()
            }
        }
    })
})
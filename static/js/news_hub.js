document.addEventListener("DOMContentLoaded", function () {
    // --- Dropdown Logic ---
    const wrapper = document.getElementById('category-wrapper');
    const dropdown = document.getElementById('category-dropdown');
    const selected = dropdown?.querySelector('.dropdown-selected');
    const options = dropdown?.querySelectorAll('.dropdown-options li');
    const label = document.getElementById('category-label');

    let hoverTimeout = null;

    if (label) {
        label.addEventListener('click', () => {
            wrapper.classList.toggle('open');
        });
    }

    if (selected) {
        selected.addEventListener('click', () => {
            wrapper.classList.toggle('open');
        });
    }

    if (wrapper) {
        wrapper.addEventListener('mouseenter', () => {
            clearTimeout(hoverTimeout);
            wrapper.classList.add('open');
        });

        wrapper.addEventListener('mouseleave', () => {
            hoverTimeout = setTimeout(() => {
                wrapper.classList.remove('open');
            }, 200);
        });
    }

    document.addEventListener('click', (e) => {
        if (wrapper && !wrapper.contains(e.target)) {
            wrapper.classList.remove('open');
        }
    });

    if (options) {
        options.forEach(option => {
            option.addEventListener('click', () => {
                selected.textContent = option.textContent;
                wrapper.classList.remove('open');
                // Update the actual select element for filtering
                const select = document.getElementById('news-category');
                if (select) select.value = option.getAttribute('data-value') || option.textContent.toLowerCase();
                select?.dispatchEvent(new Event('change'));
            });
        });
    }

    // --- AI Chat Logic ---
    const chatInput = document.getElementById('chat-input');
    const chatSend = document.getElementById('chat-send');
    const chatMessages = document.getElementById('chat-messages');
    const select = document.getElementById('news-category');

    function appendMessage(user, text){
        const div = document.createElement('div');
        div.innerHTML = `<b>${user}:</b> ${text}`;
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function sendMessage(){
        const message = chatInput.value.trim();
        if(!message) return;
        appendMessage('You', message);
        chatInput.value = '';

        const category = select ? select.value : null;
        console.log("Sending message:", message, "Category:", category);

        fetch("/chat_ai/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({message: message, category: category})
        })
        .then(res => res.json())
        .then(data => {
            console.log("AI response:", data);
            appendMessage('AI', data.reply || 'No response from AI.');
        })
        .catch(err => {
            console.error(err);
            appendMessage('AI', 'Sorry, something went wrong.');
        });
    }

    chatSend.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', e => { if(e.key === 'Enter') sendMessage(); });

    select?.addEventListener('change', () => {
        console.log("Selected category:", select.value);
        // Optional: trigger additional filtering logic here
    });

    // --- Media Click Logic ---
    const mediaModal = document.getElementById('mediaModal');
    const mediaContainer = document.getElementById('modalMediaContainer');
    const mediaClose = document.getElementById('modalClose');

    document.querySelectorAll('.clickable-media').forEach(media => {
        media.style.cursor = 'pointer';
        media.addEventListener('click', () => {
            const type = media.getAttribute('data-type');
            const src = media.getAttribute('data-src');

            mediaContainer.innerHTML = '';

            if (type === 'image') {
                const img = document.createElement('img');
                img.src = src;
                mediaContainer.appendChild(img);
            } else if (type === 'video') {
                const video = document.createElement('video');
                video.src = src;
                video.controls = true;
                video.autoplay = true;
                mediaContainer.appendChild(video);
            }

            mediaModal.style.display = 'flex';
        });
    });

    mediaClose?.addEventListener('click', () => {
        mediaModal.style.display = 'none';
        mediaContainer.innerHTML = '';
    });

    mediaModal?.addEventListener('click', (e) => {
        if (e.target === mediaModal) {
            mediaModal.style.display = 'none';
            mediaContainer.innerHTML = '';
        }
    });
});

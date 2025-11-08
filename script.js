// Matrix effect simulation
document.addEventListener('DOMContentLoaded', function() {
    // Add typing effect to headings
    const headings = document.querySelectorAll('h1, h2');
    headings.forEach(heading => {
        const text = heading.textContent;
        heading.textContent = '';
        let i = 0;
        const typeWriter = () => {
            if (i < text.length) {
                heading.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 100);
            }
        };
        setTimeout(typeWriter, 500);
    });
});

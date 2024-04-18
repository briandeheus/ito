module.exports = {
    content: [
        "./templates/*.{html,js}",
        "./templates/partials/*.{html,js}"
    ],
    theme: {
        extend: {},
    },
    plugins: [
        require('@tailwindcss/typography'),
    ],
}
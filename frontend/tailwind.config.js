module.exports = {
    content: [
        './app/**/*.{vue,js,ts}',       // ← ajouté pour Nuxt 3 / le dossier app/
        './components/**/*.{vue,js,ts}',
        './layouts/**/*.{vue,js,ts}',
        './pages/**/*.{vue,js,ts}',
        './plugins/**/*.{js,ts}',
        './nuxt.config.{js,ts}'
    ],
    theme: {
        extend: {
            colors: {
                airbnb: {
                    rose: '#FF5A5F',
                    mint: '#00A699',
                    orange: '#FC642D',
                    graylight: '#F7F7F7',
                    gray: '#767676',
                    graydark: '#484848'
                }
            },
            fontFamily: {
                circular: ['Circular', 'Helvetica Neue', 'sans-serif']
            },
            boxShadow: {
                sm: '0 1px 2px 0 rgba(72,72,72,0.04)'
            }
        }
    },
    plugins: [],
}
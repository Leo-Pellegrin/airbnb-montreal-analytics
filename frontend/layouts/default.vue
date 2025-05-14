<template>
    <div class="flex h-screen">
        <!-- Sidebar fixe à gauche -->
        <Sidebar class="w-64 border-r" />

        <!-- Conteneur principal : header + page -->
        <div class="flex-1 flex flex-col min-h-0">
            <!-- Header en haut -->
            <Header />

            <!-- Zone de contenu qui prend tout le reste, avec scroll si besoin -->
            <div class="flex-1 overflow-auto min-h-0">
                <!-- C’est ici que s’affiche ta page -->
                <NuxtPage />
            </div>
        </div>
    </div>
</template>
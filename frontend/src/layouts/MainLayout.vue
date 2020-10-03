<template>
    <div class="np-main-layout">
        <div class="np-main-layout-grid">
            <div class="np-main-layout-sidebar">
                <np-sidebar></np-sidebar>
            </div>
            <div class="np-main-layout-header">
                <np-header></np-header>
            </div>
            <div class="np-main-layout-content">
                <slot></slot>
            </div>
            <div class="np-main-layout-footer"></div>
        </div>
    </div>
</template>

<script>
import NpSidebar from '@/components/NpSidebar.vue';
import NpHeader from '@/components/NpHeader.vue';

export default {
    components: {
        NpSidebar,
        NpHeader
    }
}
</script>

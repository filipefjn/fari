<template>
    <div class="np-sidebar">
        <np-sidebar-item :names="['Home']"    path="/"        title="Home"></np-sidebar-item>
        <np-sidebar-item :names="['Artists']" path="/artists" title="Artists"></np-sidebar-item>
        <np-sidebar-item :names="['Folders']" path="/folders" title="Folders"></np-sidebar-item>
        <np-sidebar-item :names="['Filter']"  path="/filter"  title="Filter"></np-sidebar-item>
        <np-sidebar-item :names="['Queue']"   path="/queue"   title="Queue"></np-sidebar-item>
        <np-sidebar-separator></np-sidebar-separator>
        <np-sidebar-item :names="['Server']"  path="/server"  title="Server"></np-sidebar-item>
    </div>
</template>

<script>
import NpSidebarItem from '@/components/NpSidebarItem.vue';
import NpSidebarSeparator from '@/components/NpSidebarSeparator.vue';

export default {
    components: {
        NpSidebarItem,
        NpSidebarSeparator
    }
}
</script>

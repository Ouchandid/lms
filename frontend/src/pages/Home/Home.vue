<template>
	<div class="w-full px-5 pt-5 pb-10">
		<div class="flex flex-col items-center text-center py-8 mb-4 home-hero">
			<img
				:src="ministryLogo"
				class="h-64 w-auto mb-4"
				style="filter: drop-shadow(0 4px 10px rgba(11, 85, 64, 0.25))"
			/>
			<div class="home-hero-title">منصة التعليم الثانوي العتيق</div>
		</div>

		<div class="marquee-wrap">
			<div class="marquee-track">
				<span class="marquee-item">{{ marqueeText }}</span>
				<span class="marquee-item">{{ marqueeText }}</span>
			</div>
		</div>

		<div
			v-if="isHomeLoading"
			class="flex flex-1 items-center justify-center py-20"
		>
			<LoadingIndicator class="size-5 text-ink-gray-5" />
		</div>
		<AdminHome
			v-else-if="isAdmin && currentTab === 'instructor'"
			:liveClasses="adminLiveClasses"
			:evals="adminEvals"
		/>
		<StudentHome
			v-else-if="currentTab === 'student'"
			:myLiveClasses="myLiveClasses"
		/>
	</div>
	<Streak v-model="showStreakModal" :streakInfo="streakInfo" />
</template>
<script setup lang="ts">
import { computed, inject, onMounted, ref } from 'vue'
import { call, createResource, LoadingIndicator, usePageMeta } from 'frappe-ui'
import { sessionStore } from '@/stores/session'
import StudentHome from '@/pages/Home/StudentHome.vue'
import AdminHome from '@/pages/Home/AdminHome.vue'
import Streak from '@/pages/Home/Streak.vue'
import ministryLogo from '@/assets/images/logo.png'

const user = inject<any>('$user')
const { brand } = sessionStore()
const marqueeText =
	'📚 مرحبًا بكم في منصة التعليم الثانوي العتيق | يمكنكم متابعة الدروس والمحاضرات والاختبارات من خلال المنصة | نسأل الله لكم التوفيق والسداد في طلب العلم.'
const evalCount = ref(0)
const currentTab = ref<'student' | 'instructor'>('student')
const showStreakModal = ref(false)

const fetchEvalCount = () => {
	call('frappe.client.get_count', {
		doctype: 'LMS Certificate Request',
		filters: {
			member: user?.data?.name,
			status: 'Upcoming',
			date: ['>=', inject<any>('$dayjs')().format('YYYY-MM-DD')],
		},
	}).then((data: any) => {
		evalCount.value = data
	})
}

const isAdmin = computed(() => {
	return (
		user.data?.is_moderator ||
		user.data?.is_instructor ||
		user.data?.is_evaluator
	)
})

const isHomeLoading = computed(() => {
	if (isAdmin.value) {
		return (
			(adminLiveClasses.loading && !adminLiveClasses.data) ||
			(adminEvals.loading && !adminEvals.data)
		)
	}
	return myLiveClasses.loading && !myLiveClasses.data
})

onMounted(() => {
	if (isAdmin.value) {
		currentTab.value = 'instructor'
	} else {
		currentTab.value = 'student'
		fetchEvalCount()
	}
})

const myLiveClasses = createResource({
	url: 'lms.lms.api.get_my_live_classes',
	auto: !isAdmin.value ? true : false,
})

const adminLiveClasses = createResource({
	url: 'lms.lms.api.get_admin_live_classes',
	auto: isAdmin.value ? true : false,
})

const adminEvals = createResource({
	url: 'lms.lms.api.get_admin_evals',
	auto: isAdmin.value ? true : false,
})

const streakInfo = createResource({
	url: 'lms.lms.api.get_streak_info',
	auto: true,
})

const subtitle = computed(() => {
	if (isAdmin.value) {
		let liveClassSuffix =
			adminLiveClasses.data?.length > 1 ? __('live classes') : __('live class')
		let evalSuffix =
			adminEvals.data?.length > 1 ? __('evaluations') : __('evaluation')
		if (adminLiveClasses.data?.length > 0 && adminEvals.data?.length > 0) {
			return __('You have {0} upcoming {1} and {2} {3} scheduled.').format(
				adminLiveClasses.data.length,
				liveClassSuffix,
				adminEvals.data.length,
				evalSuffix
			)
		} else if (adminLiveClasses.data?.length > 0) {
			return __('You have {0} upcoming {1}.').format(
				adminLiveClasses.data.length,
				liveClassSuffix
			)
		} else if (adminEvals.data?.length > 0) {
			return __('You have {0} {1} scheduled.').format(
				adminEvals.data.length,
				evalSuffix
			)
		}
		return __('Manage your courses and batches at a glance')
	} else {
		let liveClassSuffix =
			myLiveClasses.data?.length > 1 ? __('live classes') : __('live class')
		let evalSuffix = evalCount.value > 1 ? __('evaluations') : __('evaluation')
		if (myLiveClasses.data?.length > 0 && evalCount.value > 0) {
			return __('You have {0} upcoming {1} and {2} {3} scheduled.').format(
				myLiveClasses.data.length,
				liveClassSuffix,
				evalCount.value,
				evalSuffix
			)
		} else if (myLiveClasses.data?.length > 0) {
			return __('You have {0} upcoming {1}.').format(
				myLiveClasses.data.length,
				liveClassSuffix
			)
		} else if (evalCount.value > 0) {
			return __('You have {0} {1} scheduled.').format(
				evalCount.value,
				evalSuffix
			)
		}
		return __('Resume where you left off')
	}
})

usePageMeta(() => {
	return {
		title: __('Home'),
		icon: brand.favicon,
	}
})
</script>
<style>
.home-hero-title {
	font-family: 'maghribiassile';
	color: #0b5540;
	font-size: 50px;
	line-height: 60px;
	text-align: center;
	margin-top: 30px;
}

.marquee-wrap {
	overflow: hidden;
	white-space: nowrap;
	background: linear-gradient(90deg, #0f6b4f, #0b5540);
	border-radius: 10px;
	padding: 12px 0;
	direction: ltr;
}
.marquee-track {
	display: inline-flex;
	white-space: nowrap;
	animation: marquee-rtl 28s linear infinite;
}
.marquee-item {
	display: inline-block;
	padding-inline-end: 4rem;
	white-space: nowrap;
	color: #fff;
	font-weight: 600;
	font-size: 1.05rem;
	direction: rtl;
}
@keyframes marquee-rtl {
	from {
		transform: translateX(-50%);
	}
	to {
		transform: translateX(0);
	}
}
</style>

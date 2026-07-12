<template>
	<div
		v-if="course.title"
		class="flex flex-col h-full rounded-md overflow-hidden text-ink-gray-9 shadow-sm"
		style="min-height: 350px"
	>
		<div
			class="relative w-[100%] h-[190px] overflow-hidden course-card-thumb"
			:class="brandTone"
			:style="course.image ? { backgroundImage: `url(${course.image})` } : {}"
		>
			<template v-if="!course.image">
				<div class="course-card-thumb-pattern" />
				<span class="course-card-thumb-icon" :class="brandIcon" />
			</template>
			<div class="course-card-thumb-scrim" />

			<span class="course-card-badge-icon" :class="brandIcon" />

			<div
				v-if="badgeLabel"
				class="absolute top-2.5 inset-inline-end-2.5 flex items-center gap-1.5 bg-surface-white/90 text-ink-gray-8 text-xs font-medium px-2.5 py-1 rounded-full shadow-sm"
			>
				<span class="size-1.5 rounded-full bg-surface-green-3" />
				{{ badgeLabel }}
			</div>

			<div class="course-card-thumb-title">
				<div
					class="font-semibold leading-6 text-white"
					:class="course.title.length > 32 ? 'text-lg' : 'text-2xl'"
				>
					{{ course.title }}
				</div>
				<div class="short-introduction text-sm text-white/85">
					{{ course.short_introduction }}
				</div>
			</div>
		</div>
		<div
			class="flex flex-col flex-auto p-4 course-card-footer"
			:class="brandTone"
		>
			<div class="flex items-center justify-between mb-2 text-white/90">
				<div v-if="course.lessons">
					<Tooltip :text="__('Lessons')">
						<span class="flex items-center">
							<span class="lucide-book-open size-4 me-1" />
							{{ course.lessons }}
						</span>
					</Tooltip>
				</div>

				<div v-if="course.enrollments">
					<Tooltip :text="__('Enrolled Students')">
						<span class="flex items-center">
							<span class="lucide-users size-4 me-1" />
							{{ formatAmount(course.enrollments) }}
						</span>
					</Tooltip>
				</div>

				<div v-if="course.rating">
					<Tooltip :text="__('Average Rating')">
						<span class="flex items-center">
							<LucideStar class="size-4 me-1 text-transparent fill-yellow-400" />
							{{ formatRating(course.rating) }}
						</span>
					</Tooltip>
				</div>

				<Tooltip v-if="course.featured" :text="__('Featured')">
					<span class="lucide-award size-4 text-ink-amber-6" />
				</Tooltip>
			</div>

			<ProgressBar
				v-if="user && course.membership"
				:progress="course.membership.progress"
			/>

			<div
				v-if="user && course.membership"
				class="text-sm mt-2 mb-4 text-white/90"
			>
				{{ Math.ceil(course.membership.progress) }}% {{ __('completed') }}
			</div>

			<div class="flex items-center justify-between mt-auto">
				<div class="flex avatar-group overlap">
					<div
						class="h-6 me-1"
						:class="{ 'avatar-group overlap': course.instructors.length > 1 }"
					>
						<UserAvatar
							v-for="instructor in course.instructors"
							:user="instructor"
						/>
					</div>
					<CourseInstructors :instructors="course.instructors" />
				</div>

				<div class="flex items-center gap-x-2">
					<div v-if="course.paid_course" class="font-semibold text-white">
						{{ course.price }}
					</div>

					<Tooltip
						v-if="course.paid_certificate || course.enable_certification"
						:text="__('Get Certified')"
					>
						<span class="lucide-graduation-cap size-5 text-white/90" />
					</Tooltip>
				</div>
			</div>
		</div>
	</div>
</template>
<script setup>
import { sessionStore } from '@/stores/session'
import { Tooltip } from 'frappe-ui'
import { formatAmount, formatRating } from '@/utils'
import { computed } from 'vue'
import CourseInstructors from '@/components/CourseInstructors.vue'
import UserAvatar from '@/components/UserAvatar.vue'
import ProgressBar from '@/components/ProgressBar.vue'

const { user } = sessionStore()

const props = defineProps({
	course: {
		type: Object,
		default: null,
	},
})

// Real photo covers when the course has one (course.image), with a
// gradient-tinted scrim so the white title text stays legible; falls back
// to the brand gradient + zellige pattern + icon for courses without a
// cover. Tone alternates deterministically per course so a course list
// doesn't render as a wall of identical cards, and carries through to the
// footer so the whole card reads as one colored unit instead of a photo
// glued onto a plain white box.
const toneList = ['navy', 'emerald']
const brandTone = computed(() => {
	const key = props.course.name || props.course.title || ''
	let hash = 0
	for (let i = 0; i < key.length; i++) hash = (hash + key.charCodeAt(i)) % toneList.length
	return `course-card-thumb--${toneList[hash]}`
})
const brandIcon = computed(() => 'lucide-book-open')
const badgeLabel = computed(() => props.course.category || '')
</script>
<style>
.course-card-thumb {
	background-size: cover;
	background-position: center;
}
.course-card-thumb--navy {
	background-image: linear-gradient(160deg, #123150 0%, #0b2137 70%, #0a1929 100%);
}
.course-card-thumb--emerald {
	background-image: linear-gradient(160deg, #14795c 0%, #0a4d39 70%, #0b2137 100%);
}
.course-card-footer.course-card-thumb--navy {
	background-image: linear-gradient(180deg, #0b2137, #081a2c);
}
.course-card-footer.course-card-thumb--emerald {
	background-image: linear-gradient(180deg, #0a4d39, #072e23);
}
.course-card-thumb-scrim {
	position: absolute;
	inset: 0;
	background-image: linear-gradient(
		180deg,
		rgba(10, 20, 30, 0.05) 0%,
		rgba(10, 20, 30, 0.35) 55%,
		rgba(10, 20, 30, 0.85) 100%
	);
}
.course-card-thumb-pattern {
	position: absolute;
	inset: 0;
	background-image: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHdpZHRoPSc2NCcgaGVpZ2h0PSc2NCcgdmlld0JveD0nMCAwIDY0IDY0Jz48ZyBmaWxsPSdub25lJyBzdHJva2U9JyMwRjZCNEYnIHN0cm9rZS13aWR0aD0nMS4xJyBvcGFjaXR5PScwLjUnPjxyZWN0IHg9JzE2JyB5PScxNicgd2lkdGg9JzMyJyBoZWlnaHQ9JzMyJy8+PHJlY3QgeD0nMTYnIHk9JzE2JyB3aWR0aD0nMzInIGhlaWdodD0nMzInIHRyYW5zZm9ybT0ncm90YXRlKDQ1IDMyIDMyKScvPjxjaXJjbGUgY3g9JzMyJyBjeT0nMzInIHI9JzYnLz48L2c+PC9zdmc+');
	background-size: 42px 42px;
	opacity: 0.35;
	filter: brightness(4);
	mask-image: radial-gradient(circle at 50% 45%, transparent 0%, transparent 22%, black 55%);
	-webkit-mask-image: radial-gradient(
		circle at 50% 45%,
		transparent 0%,
		transparent 22%,
		black 55%
	);
}
.course-card-thumb-icon {
	position: absolute;
	top: 50%;
	left: 50%;
	transform: translate(-50%, -50%);
	width: 44px;
	height: 44px;
	color: rgba(255, 255, 255, 0.85);
}
.course-card-badge-icon {
	position: absolute;
	top: 10px;
	inset-inline-start: 10px;
	width: 30px;
	height: 30px;
	padding: 6px;
	box-sizing: border-box;
	color: #fff;
	background: rgba(255, 255, 255, 0.18);
	backdrop-filter: blur(2px);
	border-radius: 8px;
}
.course-card-thumb-title {
	position: absolute;
	inset-inline: 0;
	bottom: 0;
	padding: 12px 14px 14px;
}

/* CourseInstructors/UserAvatar default to text-ink-gray-7, a muted gray
   meant for light cards — illegible on the footer's dark navy/emerald
   background, so force it light here. */
.course-card-footer .text-ink-gray-7,
.course-card-footer .text-ink-gray-6,
.course-card-footer .text-ink-gray-5 {
	color: rgba(255, 255, 255, 0.85) !important;
}
.course-card-footer .text-ink-gray-7:hover {
	color: #fff !important;
}

.course-card-pills {
	background: #ffffff;
	margin-left: 0;
	margin-right: 0.5rem;
	padding: 3.5px 8px;
	font-size: 11px;
	text-align: center;
	letter-spacing: 0.011em;
	text-transform: uppercase;
	font-weight: 600;
	width: fit-content;
}

.avatar-group {
	display: inline-flex;
	align-items: center;
}

.avatar-group .avatar {
	transition: margin 0.1s ease-in-out;
}

.avatar-group.overlap .avatar + .avatar {
	margin-inline-start: calc(-8px);
}

.short-introduction {
	display: -webkit-box;
	-webkit-line-clamp: 2;
	-webkit-box-orient: vertical;
	text-overflow: ellipsis;
	width: 100%;
	overflow: hidden;
	line-height: 1.4;
}
</style>

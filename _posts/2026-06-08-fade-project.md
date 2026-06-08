---
title: "FADE: Foreground Attention Decoupling for Object Generation in Training-Free Image Editing"
date: 2026-06-08
categories: [Project]
tags: [Image Editing, Diffusion, Attention, Training-Free, FADE]
description: "Training-free 이미지 편집에서 전경 어텐션을 분리해 객체를 자연스럽게 생성하는 FADE 방법론 소개."
---

<div style="position:relative;width:100%;padding-top:57.76%;margin:2rem 0;border-radius:12px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.18);">
  <iframe
    src="https://docs.google.com/presentation/d/e/2PACX-1vQiraWxGMfMfn9k3YpEKbZSYLhBGf98fpC6i-fJtVr4_2ti9DzlDvbOg399RM5UBA/pubembed?start=false&loop=false&delayms=3000"
    style="position:absolute;top:0;left:0;width:100%;height:100%;border:none;"
    frameborder="0"
    allowfullscreen="true"
    mozallowfullscreen="true"
    webkitallowfullscreen="true">
  </iframe>
</div>

## 한 줄 요약

**FADE**는 추가 학습 없이 (Training-Free), diffusion 모델의 **어텐션 맵을 전경(foreground)과 배경(background)으로 분리**함으로써, 원하는 객체를 이미지 안에 자연스럽게 삽입·생성하는 이미지 편집 방법론이다.

## 문제 의식

기존 training-free 이미지 편집 방법들은 diffusion 모델의 cross-attention과 self-attention을 조작해 객체를 삽입하지만, **전경 객체의 어텐션이 배경 영역을 침범**하거나 반대로 배경 어텐션이 객체 영역을 훼손하는 문제가 발생한다.

- 새 객체를 삽입할 때 배경이 왜곡되거나
- 객체 자체의 형태·텍스처가 배경에 묻혀 흐릿해지는 현상

이는 어텐션이 전경·배경을 구분하지 않고 전역적으로 계산되기 때문이다.

## 핵심 아이디어: Foreground Attention Decoupling

FADE의 핵심은 **전경 어텐션과 배경 어텐션을 명시적으로 분리(decouple)** 하는 것이다.

1. **Foreground Mask 추출** — 편집 대상 객체 영역을 어텐션 맵 또는 segmentation 기반으로 분리
2. **Attention Decoupling** — 전경 영역의 self-attention은 객체 내부끼리만, 배경 영역은 배경끼리만 참조하도록 제한
3. **Training-Free** — LoRA·파인튜닝 없이 추론 단계(inference)에서만 어텐션 조작으로 적용

## 왜 효과적인가

- 전경·배경 어텐션이 서로 간섭하지 않으므로 **배경 보존율이 높아짐**
- 새 객체가 본래 텍스처·형태를 잃지 않고 **삽입 품질이 향상됨**
- 추가 학습 비용 없이 기존 diffusion 모델(SDXL 등)에 바로 적용 가능

## 한 줄 정리

> 어텐션을 전경과 배경으로 나눠서 계산하면, 객체 삽입 시 배경도 살고 객체도 산다.

---

*구체적인 수식·정량 실험 결과는 슬라이드를 참고하세요.*

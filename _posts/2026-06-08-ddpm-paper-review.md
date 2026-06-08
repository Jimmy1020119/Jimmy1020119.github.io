---
title: "[Review] Denoising Diffusion Probabilistic Models (DDPM)"
date: 2026-06-08
categories: [Paper Review]
tags: [Diffusion, Generative Model, DDPM, Score Matching, Image Generation]
description: "Ho et al. (2020) — the paper that put diffusion models on the map for high-quality image generation."
---

<div style="position:relative;width:100%;padding-top:57.76%;margin:2rem 0;border-radius:12px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.18);">
  <iframe
    src="https://docs.google.com/presentation/d/e/2PACX-1vTGWN01nz7ygVGRE_jQlLK_aExHC3-C9lHD6wXpQ0xRRuntKVbJ0e5llkaic1I3x9UhzltSnSuIf-uv/pubembed?start=false&loop=false&delayms=3000"
    style="position:absolute;top:0;left:0;width:100%;height:100%;border:none;"
    frameborder="0"
    allowfullscreen="true"
    mozallowfullscreen="true"
    webkitallowfullscreen="true">
  </iframe>
</div>

---

## English Summary

### TL;DR
DDPM (Ho et al., NeurIPS 2020) showed that **diffusion probabilistic models** can generate high-quality images competitive with GANs by learning to reverse a gradual noising process — without adversarial training.

### Background
Diffusion models had been proposed theoretically (Sohl-Dickstein et al., 2015), but had not yet demonstrated strong image synthesis quality. DDPM was the paper that closed this gap.

### The Core Idea

**Forward Process (Diffusion)**
Starting from a clean image $x_0$, Gaussian noise is added step-by-step over $T$ timesteps:

$$q(x_t \mid x_{t-1}) = \mathcal{N}(x_t;\ \sqrt{1-\beta_t}\, x_{t-1},\ \beta_t \mathbf{I})$$

After enough steps, $x_T$ is approximately pure Gaussian noise — structure is completely destroyed.

**Reverse Process (Denoising)**
A neural network $\epsilon_\theta$ (U-Net) is trained to predict the noise added at each step, so the reverse trajectory can be run:

$$p_\theta(x_{t-1} \mid x_t) = \mathcal{N}(x_{t-1};\ \mu_\theta(x_t, t),\ \Sigma_\theta)$$

**Training Objective**
Instead of optimizing the full variational lower bound, the authors found a simpler surrogate works better — just predict the added noise:

$$\mathcal{L}_{\text{simple}} = \mathbb{E}_{t, x_0, \epsilon}\left[\|\epsilon - \epsilon_\theta(\sqrt{\bar\alpha_t}\, x_0 + \sqrt{1-\bar\alpha_t}\, \epsilon,\; t)\|^2\right]$$

This is essentially **denoising score matching** at multiple noise levels.

### Key Results
- Achieved FID of **3.17** on CIFAR-10 (surpassing many GAN variants at the time)
- High-quality 256×256 image synthesis on LSUN and CelebA-HQ
- Showed that the objective is equivalent to a **weighted sum of denoising score matching** losses

### Connections
- Equivalent to learning the **score function** $\nabla_{x_t} \log p(x_t)$ at each noise level
- Directly connects to **score-based generative models** (Song & Ermon, 2019)
- Foundation for **DDIM**, **Stable Diffusion**, **DALL·E 2**, **Imagen**, and essentially all modern text-to-image systems

---

## 한국어 요약

### 한 줄 요약
DDPM은 이미지에 노이즈를 점점 더하는 과정(forward)을 학습하고, 그 역방향(reverse)으로 노이즈를 제거해가며 이미지를 생성하는 방법으로, GAN 없이도 고품질 이미지를 만들 수 있음을 처음으로 입증한 논문이다.

### 문제 의식
GAN은 학습 불안정성(mode collapse, training instability)이 심각한 단점이었다. VAE는 안정적이지만 생성 품질이 흐릿했다. Diffusion 모델은 이론적으로 존재했지만, 당시까지 이미지 생성 품질이 GAN에 한참 뒤처져 실용적이지 않다고 여겨졌다.

### 핵심 아이디어

**Forward Process (노이즈 추가)**
원본 이미지 $x_0$에서 시작해 매 스텝마다 Gaussian 노이즈를 조금씩 추가한다.
$T$ 스텝 이후 $x_T$는 완전한 랜덤 노이즈가 된다.
이 과정은 **고정(fixed)**되어 있어 학습 대상이 아니다.

**Reverse Process (노이즈 제거)**
순수 노이즈 $x_T$에서 시작해 U-Net이 매 스텝마다 노이즈를 예측하고 제거하면서 $x_0$를 복원한다.
이 역방향 과정의 파라미터 $\theta$를 학습한다.

**학습 목표 단순화**
이론적인 ELBO 대신 단순히 **각 스텝에서 더해진 노이즈 자체를 예측**하게 하는 단순화된 손실 함수를 사용 → 실험적으로 오히려 더 좋은 결과.

### 왜 중요한가

| | GAN | DDPM |
|---|---|---|
| 학습 안정성 | ❌ 불안정 | ✅ 안정적 |
| 생성 다양성 | ❌ Mode collapse | ✅ 다양함 |
| 이론적 근거 | 약함 | ✅ 확률론적 기반 |
| 생성 속도 | ✅ 빠름 | ❌ 느림 (T 스텝 필요) |

### 영향력
DDPM 이후 등장한 거의 모든 이미지 생성 모델의 뿌리가 됐다.
- **DDIM** — 생성 속도 개선 (10~50배)
- **Stable Diffusion** — 잠재 공간(latent space)으로 확장
- **DALL·E 2, Imagen** — 텍스트 조건 추가
- **ControlNet, LoRA** 등 파생 연구 전부 DDPM 위에 구축

### 한 줄 정리
> 노이즈 추가 과정을 T번 반복하면 아무 이미지나 노이즈가 된다. 그 역방향을 U-Net으로 배우면 노이즈에서 이미지를 만들 수 있다 — 이것이 현재 생성 AI의 근간이다.

---

*정량 수치 및 구체적인 알고리즘은 슬라이드를 참고하세요.*

## Transport theorem


$$
d_t \int_\Omega \phi dV = \int_\Omega\partial_t \phi +\nabla\cdot (\phi\otimes v)dV = \int_\Omega\partial_t \phi dV +\int_{\partial\Omega}\phi \langle v, dA\rangle = \int_\Omega s_\Omega dV+\int_{\partial\Omega} s_{\partial\Omega} dA\label{eq:transport}\\
$$
$$
|\Omega|\partial_t\bar{\phi} = |\Omega|\bar{s_\Omega}+\sum_f|\partial\Omega_f|\langle(s_{\partial\Omega} - \phi v)_f,n_f\rangle\label{eq:fvm}
$$
One should use operator splitting to be able to solve without the volume source term first.

#### Transport equations

- ordered basis of species $\mathcal{S}$, called $\mathrm{species}$
- species $s\in\mathcal{S}$ with 
  - mass fraction $Y_s$
  - molar fraction $X_s$
  - mass production rate $\omega_s$
  - enthalpy per unit mass $h_s$
  - force per unit mass $a_s$, usually gravitational acceleration $\bold{a}_s\ = \bold{g} = - \nabla (gz)$
- diffusion matrix $D$ with component $D_{ab}$ being cross-diffusion of species $a$ with respect to species $b$, $(a,b)\in\mathrm{species}\times\mathrm{species}$
- species thermal diffusion $\theta$, where component $\theta_a$ is thermal diffusion of species $a$
- species thermal diffusion ratios $\chi = D^{-1}\theta$, where component $\chi_a$ is thermal diffusion ratio of species $a$
- thermal conductivity $\lambda$
- absolute temperature $T$
- thermodynamic pressure $p$

Multicomponent variables:
$$
\begin{align}
X_a &= \frac{(\rho_{N})_a}{\rho_{N}}\\

Y_a &= \frac{(\rho_m)_a}{\rho_m}\\

q =&\left[\sum_{a\in\mathrm{species}}((\phi_m) h + p\chi V)_a\right]-\lambda\nabla T \\

V_a =&\left[\sum_{b\in\mathrm{species}}D_{ab}\left[\nabla(X_b) +\frac{1}{p}\left[(X_b -Y_b)\nabla(p) + (\phi_m)_b\sum_{c\in\mathrm{species}}Y_c(a_c - a_b)\right]\right]\right]+\theta_a\frac{1}{T}\nabla(T)
\end{align}
$$

Mass transport:
$$
\begin{align}
(\phi_m)_a &= \rho_mY_a\\

((s_{\partial\Omega})_m)_a &= (\phi_m)_aV_a\\

((s_\Omega)_m)_a &= \omega_a\\
\end{align}
$$

Momentum transport:
$$
\begin{align}
(\phi_p)^k =&\; \rho v^k\\

((s_{\partial\Omega})_p)_{ij} =&\; (\sigma_\mathrm{static})_{ij} + (\sigma_\mathrm{elastic})_{ij} + 

(\sigma_\mathrm{viscous})_{ij}\\

(\sigma_\mathrm{static})_{ij}=&-pg_{ij}\\

(\sigma_\mathrm{elastic})_{ij}\stackrel{?}{=}&
\frac{1}{2}[\partial_j(x-x_0)_i + \partial_i(x-x_0)_j - \partial_i(x-x_0)_k\partial_j(x-x_0)_k]\\

(\sigma_\mathrm{viscous})_{ij}=& \mu \nabla_i(g_{jk}v^k) + \mu\nabla_j(g_{ik}v^k) + \lambda\nabla_k(g_{km}v^m)g_{ij}\\

((s_\Omega)_p)_i =& \sum_{s\in\mathrm{species}}(\rho_m \cdot a_i)_s
\end{align}
$$
Energy transport:
$$
\begin{align}
\phi_E =& \left[\sum_{s\in\mathrm{species}}(\rho_m h)_s\right] - p + \frac{1}{2}\langle\rho_m v, v\rangle\\

(s_{\partial\Omega})_E =& -q+\langle \sigma, v\rangle\\

(s_\Omega)_E =& \sum_{s\in\mathrm{species}}\langle (\rho_mv + \rho_m V)_s, (a)_s \rangle\\
\end{align}
$$



#### Jacobian of divergence term with respect to material property

##### Shallow water equations

$$
p = \rho f_z h
$$



Need Jacobian for Riemann Solvers
$$
\frac{\partial(\sigma-\rho v^i v^j)}{\partial (\rho v^i)} \stackrel{?}{=} -v^j
$$


Finite Volume Method


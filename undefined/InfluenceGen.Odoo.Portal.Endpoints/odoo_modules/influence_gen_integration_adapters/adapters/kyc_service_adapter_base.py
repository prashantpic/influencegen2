# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import abc
from odoo import models, api
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..dtos.kyc_dtos import KycVerificationRequestDto, KycVerificationResultDto


class KycServiceAdapterBase(models.AbstractModel):
    """
    Abstract Base Class for KYC (Know Your Customer) service adapters.

    This class defines the contract that all concrete KYC service adapter
    implementations must adhere to. It promotes a consistent interface for
    interacting with various external KYC verification services.

    REQ-IL-011: Define common interface for KYC service adapters.
    REQ-IOKYC-005: Support KYC verification process.
    """
    _name = 'influence_gen.kyc.service.adapter.base'
    _description = 'InfluenceGen KYC Service Adapter Base'

    @abc.abstractmethod
    @api.model
    def verify_identity(self, kyc_request_dto: 'KycVerificationRequestDto') -> 'KycVerificationResultDto':
        """
        Abstract method to verify an identity using an external KYC service.

        Concrete implementations of this method will handle the specific API
        calls, authentication, request/response mapping, and error handling
        for a particular KYC provider.

        :param kyc_request_dto: An instance of `KycVerificationRequestDto`
                                containing the data required for verification.
        :type kyc_request_dto: KycVerificationRequestDto
        :return: An instance of `KycVerificationResultDto` containing the
                 outcome of the verification process.
        :rtype: KycVerificationResultDto
        :raises NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError("Subclasses must implement the verify_identity method.")
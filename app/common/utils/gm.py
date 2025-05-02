# -*- coding: utf-8 -*-
"""
model: gm
description:  
author: sven
date: 2022-09-04
"""
__author__ = '474416133@qq.com'
import secrets
from pysmx.SM2 import Encrypt, Decrypt
from pysmx import SM4
from pysmx import SM3


def encrypt(public_key, word):
    """
    加密
    :param public_key:
    :param word:
    :return:
    """
    return Encrypt(word, public_key, 64, 0).hex()


def decrypt(private_key, token):
    """
    解密
    :param private_key:
    :param token:
    :return:
    """
    return Decrypt(token, private_key, 64).decode('utf-8')


encrypt_key = b'3\xfa\xf9\xe7\x0b%\xff4<M\xb3\x8e+\x1a\xbcK'


def encrypt_sm4(word):
    """
    加密
    :param encrypt_key:
    :param word:
    :return:
    """
    return SM4.sm4_crypt_ecb(SM4.ENCRYPT,
                             encrypt_key,
                             word.encode()).hex()


def decrypt_sm4(token):
    """
    解密
    :param encrypt_key:
    :param private_key:
    :param token:
    :return:
    """
    return SM4.sm4_crypt_ecb(SM4.DECRYPT,
                             encrypt_key,
                             bytes.fromhex(token)).decode()


def encrypt_sm3(msg):
    return SM3.Hash_sm3(msg)

